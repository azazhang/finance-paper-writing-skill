from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skill" / "finance-paper-writing" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from manuscript_hash import manuscript_sha256  # noqa: E402

READ_NOTE = """# Writer's integration
## Assembled manuscript
I read the complete current manuscript in reading order, including the
abstract, introduction, data and empirical design, main results, conclusion,
and the relevant principal exhibit titles, notes, and comparisons.
## Reconciliation and revisions
The question, sample, observation unit, magnitudes, inference, horizons, and
the concluding contribution were reconciled across the main sections; the
results paragraph was rewritten and its adjacent transitions checked.
"""

READER_NOTE = """# Fresh independent scholarly reading
## Question and economic answer
The manuscript asks whether diminishing covenant headroom predicts investment
while firms remain compliant. The economic result has a documented magnitude,
meaningful refinancing heterogeneity, and an appropriately bounded interpretation.
## Material communication feedback
The final introduction and results connect the economic question to the decisive
comparison. The writer reviewed the relevant transitions and resolved an obsolete
statement without starting a new referee review round.
"""


class WriterFirstFormalRecordTests(unittest.TestCase):

    def start(self, root: Path, mode: str = "full-manuscript",
              reader: bool = False, include: bool = False) -> tuple[Path, Path]:
        (root / ".git").mkdir()
        manuscript = root / "main.tex"
        if include:
            (root / "results.tex").write_text("First outcome description.\n")
            manuscript.write_text("\\input{results}\n")
        else:
            manuscript.write_text("First outcome description.\n")
        cmd = [sys.executable, str(SCRIPTS / "init_run.py"), str(manuscript),
               "--project-root", str(root), "--lead-editor", "writer-a",
               "--mode", mode]
        if reader:
            cmd.append("--with-independent-reader")
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return Path(out.stdout.splitlines()[0]), manuscript

    @staticmethod
    def rewrite(manuscript: Path, include: bool = False, suffix: str = "New result.") -> str:
        file = manuscript.parent / "results.tex" if include else manuscript
        file.write_text("First outcome description. " + suffix + "\n")
        return manuscript_sha256(manuscript)

    @staticmethod
    def update(run_dir: Path, **fields) -> None:
        path = run_dir / "run.json"
        run = json.loads(path.read_text())
        run.update(fields)
        path.write_text(json.dumps(run, indent=2) + "\n")

    @staticmethod
    def validate(run_dir: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPTS / "validate_run_state.py"),
                               str(run_dir)], capture_output=True, text=True)

    def complete_writer(self, run_dir: Path, current_hash: str) -> None:
        self.update(run_dir, final_manuscript_sha256=current_hash,
                    writer_read_sha256=current_hash)
        (run_dir / "writer-integration.md").write_text(READ_NOTE)

    def test_current_default_avoids_scores_pass_logs_and_reader(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d))
            run = json.loads((run_dir / "run.json").read_text())
            self.assertEqual(run["schema_version"], 3)
            self.assertFalse(run["independent_reader"]["requested"])
            self.assertTrue((run_dir / "writer-integration.md").is_file())
            self.assertFalse((run_dir / "pass-log.tsv").exists())
            self.assertFalse((run_dir / "cold-reader-report.md").exists())
            self.assertFalse((run_dir / "independent-reader-notes.md").exists())
            self.assertNotIn("gates", run)
            self.assertNotIn("required_edit_passes", run)
            self.assertEqual(run["baseline_manuscript_sha256"], manuscript_sha256(manuscript))

    def test_completed_writer_record_passes_without_reader(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d))
            hash_ = self.rewrite(manuscript)
            self.complete_writer(run_dir, hash_)
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("not a manuscript-quality", result.stdout)

    def test_unfilled_writer_template_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d))
            hash_ = self.rewrite(manuscript)
            self.update(run_dir, final_manuscript_sha256=hash_, writer_read_sha256=hash_)
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unfilled template", result.stdout)

    def test_stale_writer_read_rejected_after_further_edit(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d))
            previous = self.rewrite(manuscript)
            self.complete_writer(run_dir, previous)
            current = self.rewrite(manuscript, suffix="Revised estimate.")
            self.update(run_dir, final_manuscript_sha256=current)
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("integrated reading is missing or stale", result.stdout)

    def test_included_latex_file_change_detected(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d), include=True)
            first = self.rewrite(manuscript, include=True)
            self.complete_writer(run_dir, first)
            self.rewrite(manuscript, include=True, suffix="Later corrected interpretation.")
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("final manuscript hash is stale", result.stdout)

    def test_optional_reader_stays_optional_and_can_precede_final_repair(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d), reader=True)
            examined = self.rewrite(manuscript, suffix="Draft interpretation.")
            final = self.rewrite(manuscript, suffix="Revised interpretation.")
            self.complete_writer(run_dir, final)
            self.update(run_dir, independent_reader={
                "requested": True,
                "identity": "fresh-reader-b",
                "manuscript_sha256": examined,
            })
            (run_dir / "independent-reader-notes.md").write_text(READER_NOTE)
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_reader_identity_must_be_independent_when_selected(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d), reader=True)
            current = self.rewrite(manuscript)
            self.complete_writer(run_dir, current)
            self.update(run_dir, independent_reader={
                "requested": True, "identity": "writer-a",
                "manuscript_sha256": current,
            })
            (run_dir / "independent-reader-notes.md").write_text(READER_NOTE)
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("matches the writer", result.stdout)

    def test_reader_note_template_must_be_filled_when_selected(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d), reader=True)
            current = self.rewrite(manuscript)
            self.complete_writer(run_dir, current)
            self.update(run_dir, independent_reader={
                "requested": True, "identity": "reviewer-c",
                "manuscript_sha256": current,
            })
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unfilled template", result.stdout)

    def test_no_change_after_actual_integrated_read_is_valid(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d))
            current = manuscript_sha256(manuscript)
            self.complete_writer(run_dir, current)
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("formal record valid", result.stdout)

    def test_prose_audit_requires_no_writer_or_reader_files(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, _ = self.start(Path(d), mode="prose-audit")
            self.assertFalse((run_dir / "writer-integration.md").exists())
            self.assertFalse((run_dir / "independent-reader-notes.md").exists())
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_prose_audit_detects_changed_manuscript(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d), mode="prose-audit")
            self.rewrite(manuscript)
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("stale", result.stdout)

    def test_optional_linter_warnings_do_not_gate_formal_record(self):
        with tempfile.TemporaryDirectory() as d:
            run_dir, manuscript = self.start(Path(d))
            current = self.rewrite(manuscript)
            self.complete_writer(run_dir, current)
            (run_dir / "prose-lint.json").write_text(json.dumps({
                "manuscript_sha256": current, "hard_failure_count": 1,
                "warning_count": 0, "findings": [{"category": "local-path"}],
            }))
            result = self.validate(run_dir)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("assess in context", result.stdout)


if __name__ == "__main__":
    unittest.main()
