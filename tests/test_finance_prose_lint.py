from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPO_ROOT
    / "skill"
    / "finance-paper-writing"
    / "scripts"
    / "finance_prose_lint.py"
)


class FinanceProseLintTests(unittest.TestCase):
    def run_lint(self, text: str, suffix: str = ".tex") -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manuscript = root / f"main{suffix}"
            report = root / "report.json"
            manuscript.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(manuscript),
                    "--manuscript",
                    str(manuscript),
                    "--json-output",
                    str(report),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            data = json.loads(report.read_text(encoding="utf-8"))
            return result, data

    def test_clean_standard_finance_prose_passes(self) -> None:
        result, data = self.run_lint(
            r"""
\section{Results}
Firms near covenant thresholds reduce investment in the subsequent quarter.
The estimate is economically meaningful relative to average quarterly investment.
"""
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["hard_failure_count"], 0)
        self.assertEqual(data["warning_count"], 0)

    def test_development_and_local_path_leakage_fail(self) -> None:
        result, data = self.run_lint(
            r"""
\section{Data}
The v6-positive windows and generated manuscript exhibits come from /Users/name/project/output.
The human principal investigator then reviewed the locally archived files.
"""
        )
        self.assertEqual(result.returncode, 1)
        self.assertGreaterEqual(data["hard_failure_count"], 4)
        categories = {item["category"] for item in data["findings"]}
        self.assertIn("local-path", categories)
        self.assertIn("development-record", categories)
        self.assertIn("internal-version-label", categories)
        self.assertIn("awkward-author-role", categories)

    def test_defensive_section_opening_is_flagged(self) -> None:
        result, data = self.run_lint(
            r"""
\section{Closest Literature}
Although the two measures need not display perfect nesting, their overlap remains informative.
Prior work studies a narrower operating constraint.
"""
        )
        self.assertEqual(result.returncode, 0)
        categories = {item["category"] for item in data["findings"]}
        self.assertIn("negative-section-opening", categories)
        self.assertIn("defensive-phrase", categories)
        self.assertTrue(all(item["finding_id"].startswith("fpw-") for item in data["findings"]))

    def test_repeated_noncausality_language_is_flagged(self) -> None:
        result, data = self.run_lint(
            r"""
\section{Results}
The estimate is not causal.
The timing evidence is informative but not causal.
"""
        )
        self.assertEqual(result.returncode, 0)
        repeated = [
            item for item in data["findings"] if item["category"] == "repeated-disclaimer"
        ]
        self.assertEqual(len(repeated), 1)

    def test_negative_contribution_framing_is_flagged(self) -> None:
        result, data = self.run_lint(
            r"""
\section{Closest Literature}
The contribution does not rest on whether the two measures overlap perfectly.
"""
        )
        self.assertEqual(result.returncode, 0)
        categories = {item["category"] for item in data["findings"]}
        self.assertIn("negative-contribution-framing", categories)

    def test_generic_paper_does_not_trigger_measure_vocabulary(self) -> None:
        result, data = self.run_lint(
            r"""
\section{Research Design}
I compare acquisition activity around staggered changes in state antitakeover law.
Standard errors are clustered by state.
"""
        )
        self.assertEqual(result.returncode, 0)
        output = json.dumps(data).lower()
        self.assertNotIn("classifier", output)
        self.assertNotIn("kappa", output)

    def test_text_measure_checks_require_optional_module(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manuscript = root / "main.tex"
            default_report = root / "default.json"
            module_report = root / "module.json"
            manuscript.write_text(
                "The semantic teacher provides the ground truth labels.\n",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(manuscript),
                    "--json-output",
                    str(default_report),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(manuscript),
                    "--module",
                    "text-measure",
                    "--json-output",
                    str(module_report),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            default = json.loads(default_report.read_text(encoding="utf-8"))
            module = json.loads(module_report.read_text(encoding="utf-8"))
            self.assertEqual(default["warning_count"], 0)
            categories = {item["category"] for item in module["findings"]}
            self.assertIn("text-measure-internal-role", categories)
            self.assertIn("unqualified-label-truth", categories)

    def test_directory_scan_uses_only_included_tex_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            sections = root / "sections"
            sections.mkdir()
            main = root / "main.tex"
            included = sections / "results.tex"
            unused = sections / "unused.tex"
            report = root / "report.json"
            main.write_text(
                "\\section{Paper}\n\\input{sections/results}\n",
                encoding="utf-8",
            )
            included.write_text(
                "Firms reduce investment after the event.\n",
                encoding="utf-8",
            )
            unused.write_text(
                "The locally archived file is /Users/name/private.csv.\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(root),
                    "--manuscript",
                    str(main),
                    "--json-output",
                    str(report),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            data = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(data["hard_failure_count"], 0)
            self.assertNotIn(str(unused), data["files_scanned"])

    def test_main_file_target_scans_included_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            main = root / "main.tex"
            section = root / "section.tex"
            report = root / "report.json"
            main.write_text("\\input{section}\n", encoding="utf-8")
            section.write_text(
                "The locally archived file is /Users/name/private.csv.\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(main),
                    "--manuscript",
                    str(main),
                    "--json-output",
                    str(report),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            data = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 1)
            self.assertIn(str(section.resolve()), data["files_scanned"])
            self.assertGreaterEqual(data["hard_failure_count"], 2)

    def test_commented_tex_input_is_not_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            main = root / "main.tex"
            unused = root / "unused.tex"
            report = root / "report.json"
            main.write_text(
                "% \\\\input{unused}\nA clean manuscript sentence.\n",
                encoding="utf-8",
            )
            unused.write_text(
                "The locally archived file is /Users/name/private.csv.\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(main),
                    "--json-output",
                    str(report),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            data = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0)
            self.assertNotIn(str(unused.resolve()), data["files_scanned"])


if __name__ == "__main__":
    unittest.main()
