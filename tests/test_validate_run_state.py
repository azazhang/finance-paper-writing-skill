from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skill" / "finance-paper-writing"
INIT_SCRIPT = SKILL_ROOT / "scripts" / "init_run.py"
VALIDATE_SCRIPT = SKILL_ROOT / "scripts" / "validate_run_state.py"

sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from manuscript_hash import manuscript_sha256


LONG_TEXT = (
    "This completed artifact explains the economic question, the finance audience, "
    "the manuscript contribution, the main evidence, the relevant unit of observation, "
    "the supported inferential boundary, the order of the argument, the reader context, "
    "the most important qualification, and the reason the evidence changes what a "
    "finance reader knows about firm behavior and outcomes."
)


class ValidateRunStateTests(unittest.TestCase):
    def build_valid_run(
        self,
        root: Path,
        with_input: bool = False,
        module: str | None = None,
    ) -> tuple[Path, Path]:
        (root / ".git").mkdir()
        manuscript = root / "main.tex"
        if with_input:
            section = root / "results.tex"
            section.write_text(
                "\\section{Results}\nFirms reduce investment after the event.\n",
                encoding="utf-8",
            )
            manuscript.write_text("\\input{results}\n", encoding="utf-8")
        else:
            manuscript.write_text(
                "\\section{Results}\nFirms reduce investment after the event.\n",
                encoding="utf-8",
            )
        init_command = [
            sys.executable,
            str(INIT_SCRIPT),
            str(manuscript),
            "--project-root",
            str(root),
            "--lead-editor",
            "writer-a",
        ]
        if module:
            init_command.extend(["--module", module])
        init = subprocess.run(
            init_command,
            text=True,
            capture_output=True,
            check=True,
        )
        run_dir = Path(init.stdout.splitlines()[0])
        if with_input:
            (root / "results.tex").write_text(
                "\\section{Results}\nFirms reduce investment after the event. "
                "The revised prose states the economic interpretation.\n",
                encoding="utf-8",
            )
        else:
            manuscript.write_text(
                "\\section{Results}\nFirms reduce investment after the event. "
                "The revised prose states the economic interpretation.\n",
                encoding="utf-8",
            )
        current_hash = manuscript_sha256(manuscript)

        run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        baseline_hash = run["baseline_manuscript_sha256"]
        run["final_manuscript_sha256"] = current_hash
        run["gates"] = {name: "passed" for name in run["gates"]}
        (run_dir / "run.json").write_text(json.dumps(run, indent=2), encoding="utf-8")

        for name in (
            "paper-charter.md",
            "macro-prose-audit.md",
            "cold-reader-report.md",
        ):
            (run_dir / name).write_text(LONG_TEXT, encoding="utf-8")

        (run_dir / "claim-evidence-ledger.csv").write_text(
            "claim_id,economic_claim,evidence_source,exhibit,sample,unit,timing,"
            "estimate,uncertainty,provenance,verification_status,inferential_status,"
            "allowed_verbs,paper_location,caveat_home,notes\n"
            "C1,Firms reduce investment,table.csv,Table 2,Public firms,firm-quarter,"
            "subsequent quarter,-0.02,0.01,current,verified,associational,"
            "is associated with,main text,design section,\n",
            encoding="utf-8",
        )
        (run_dir / "issue-ledger.tsv").write_text(
            "issue_id\tlocation\tcategory\tseverity\tdescription\tproposed_repair\tstatus\treviewer\n",
            encoding="utf-8",
        )

        with (run_dir / "pass-log.tsv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        identities = {
            "lead_writer": "writer-a",
            "prose_referee": "reviewer-b",
            "cold_reader": "reviewer-c",
            "evidence_auditor": "reviewer-d",
        }
        for row in rows:
            row["identity"] = identities[row["role"]]
            if row["purpose"] in {"story-contract", "macro-prose-audit"}:
                row["input_sha256"] = baseline_hash
            else:
                row["input_sha256"] = current_hash
            if row["role"] == "lead_writer" and row["purpose"] != "story-contract":
                row["output_sha256"] = current_hash
            row["status"] = "completed"
        edit_rows = [
            row
            for row in rows
            if row["role"] == "lead_writer" and row["purpose"] != "story-contract"
        ]
        edit_rows[0]["input_sha256"] = baseline_hash
        with (run_dir / "pass-log.tsv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)

        (run_dir / "prose-lint.json").write_text(
            json.dumps(
                {
                    "manuscript_sha256": current_hash,
                    "hard_failure_count": 0,
                    "warning_count": 0,
                    "modules": [module] if module else [],
                    "findings": [],
                }
            ),
            encoding="utf-8",
        )
        score_lines = [
            "<!-- finance-writing-scorecard:start -->",
            f"manuscript_sha256: {current_hash}",
            "reviewer_identity: reviewer-c",
        ]
        for dimension in (
            "economic_question",
            "result_led_exposition",
            "finance_register",
            "evidence_prominence",
            "caveat_discipline",
            "reader_context",
            "closest_paper_positioning",
            "claim_calibration",
        ):
            score_lines.append(f"{dimension}_score: 2")
            score_lines.append(
                f"{dimension}_evidence: Specific manuscript evidence supports this rating"
            )
        score_lines.extend(
            [
                "applicable_dimensions: 8",
                "total_score: 16",
                "critical_failure: false",
                "decision: pass",
                "<!-- finance-writing-scorecard:end -->",
                LONG_TEXT,
            ]
        )
        (run_dir / "cold-reader-report.md").write_text(
            "\n".join(score_lines), encoding="utf-8"
        )
        (run_dir / "completion-report.md").write_text(
            f"""# Completion Report

Final manuscript: {current_hash}

| Gate | Status | Evidence |
|---|---|---|
| Evidence boundary | passed | ledger |
| Macro prose | passed | audit |
| Finance register | passed | pass log |
| Independent cold reader | passed | report |
| Evidence integrity | passed | audit |
| Rendered paper | passed | inspection |
| Convergence | passed | final read |
""",
            encoding="utf-8",
        )
        return run_dir, manuscript

    def run_validation(self, run_dir: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATE_SCRIPT), str(run_dir)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_run_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, _ = self.build_valid_run(Path(temp_dir))
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_optional_module_is_recorded_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, _ = self.build_valid_run(
                Path(temp_dir), module="text-measure"
            )
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(run["optional_modules"], ["text-measure"])
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_editing_mode_requires_a_state_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, manuscript = self.build_valid_run(Path(temp_dir))
            run_path = run_dir / "run.json"
            run = json.loads(run_path.read_text(encoding="utf-8"))
            current_hash = manuscript_sha256(manuscript)
            run["baseline_manuscript_sha256"] = current_hash
            run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
            with (run_dir / "pass-log.tsv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle, delimiter="\t"))
            for row in rows:
                if row["purpose"] in {"story-contract", "macro-prose-audit"}:
                    row["input_sha256"] = current_hash
                if row["role"] == "lead_writer" and row["purpose"] != "story-contract":
                    row["input_sha256"] = current_hash
                    row["output_sha256"] = current_hash
            with (run_dir / "pass-log.tsv").open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
                writer.writeheader()
                writer.writerows(rows)
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("no manuscript state change", result.stdout)

    def test_post_review_edit_invalidates_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, manuscript = self.build_valid_run(Path(temp_dir))
            manuscript.write_text(
                "\\section{Results}\nThe result changed after review.\n",
                encoding="utf-8",
            )
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("stale", result.stdout)

    def test_included_file_edit_invalidates_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir, _ = self.build_valid_run(root, with_input=True)
            (root / "results.tex").write_text(
                "\\section{Results}\nThe included result changed after review.\n",
                encoding="utf-8",
            )
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("stale", result.stdout)

    def test_writer_cannot_be_sole_cold_reader(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, _ = self.build_valid_run(Path(temp_dir))
            rows = []
            with (run_dir / "pass-log.tsv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle, delimiter="\t"))
            for row in rows:
                if row["purpose"] == "cold-reader":
                    row["identity"] = "writer-a"
            with (run_dir / "pass-log.tsv").open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
                writer.writeheader()
                writer.writerows(rows)
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("not independent", result.stdout)

    def test_collapsed_edit_passes_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, _ = self.build_valid_run(Path(temp_dir))
            with (run_dir / "pass-log.tsv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle, delimiter="\t"))
            rows = [row for row in rows if row["purpose"] != "anti-defense"]
            with (run_dir / "pass-log.tsv").open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
                writer.writeheader()
                writer.writerows(rows)
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("anti-defense", result.stdout)

    def test_lint_warning_requires_disposition(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, _ = self.build_valid_run(Path(temp_dir))
            lint_path = run_dir / "prose-lint.json"
            lint = json.loads(lint_path.read_text(encoding="utf-8"))
            lint["warning_count"] = 1
            lint["findings"] = [
                {
                    "finding_id": "fpw-example12345",
                    "severity": "warning",
                    "category": "defensive-phrase",
                }
            ]
            lint_path.write_text(json.dumps(lint), encoding="utf-8")
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("no disposition", result.stdout)

    def test_low_cold_reader_score_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, _ = self.build_valid_run(Path(temp_dir))
            report_path = run_dir / "cold-reader-report.md"
            report = report_path.read_text(encoding="utf-8")
            report = report.replace("_score: 2", "_score: 1")
            report = report.replace("total_score: 16", "total_score: 8")
            report_path.write_text(report, encoding="utf-8")
            result = self.run_validation(run_dir)
            self.assertEqual(result.returncode, 1)
            self.assertIn("below threshold", result.stdout)

    def test_prose_audit_initializes_nonapplicable_gates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".git").mkdir()
            manuscript = root / "main.tex"
            manuscript.write_text("\\section{Introduction}\nA finance question.\n", encoding="utf-8")
            init = subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    str(manuscript),
                    "--mode",
                    "prose-audit",
                    "--project-root",
                    str(root),
                    "--lead-editor",
                    "auditor-a",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            run_dir = Path(init.stdout.splitlines()[0])
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(
                run["final_manuscript_sha256"],
                run["baseline_manuscript_sha256"],
            )
            self.assertEqual(run["gates"]["evidence_boundary"], "not-applicable")
            self.assertEqual(run["gates"]["cold_reader"], "not-applicable")
            self.assertEqual(run["gates"]["rendered_paper"], "not-applicable")
            self.assertFalse((run_dir / "cold-reader-report.md").exists())
            self.assertFalse((run_dir / "claim-evidence-ledger.csv").exists())

    def test_section_revision_omits_full_only_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".git").mkdir()
            manuscript = root / "main.tex"
            manuscript.write_text("\\section{Introduction}\nA finance question.\n", encoding="utf-8")
            init = subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    str(manuscript),
                    "--mode",
                    "section-revision",
                    "--project-root",
                    str(root),
                    "--lead-editor",
                    "writer-a",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            run_dir = Path(init.stdout.splitlines()[0])
            self.assertFalse((run_dir / "caveat-registry.csv").exists())
            with (run_dir / "pass-log.tsv").open(encoding="utf-8", newline="") as handle:
                purposes = {row["purpose"] for row in csv.DictReader(handle, delimiter="\t")}
            self.assertNotIn("final-whole-paper-read", purposes)
            self.assertNotIn("closest-paper-positioning", purposes)


if __name__ == "__main__":
    unittest.main()
