#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED = {
    "README.md",
    "LICENSE",
    "AGENTS.md",
    "CHANGELOG.md",
    "docs/architecture.md",
    "docs/how-to-use.md",
    "docs/provider-support.md",
    "docs/project-routing-rule.md",
    "skill/finance-paper-writing/SKILL.md",
    "skill/finance-paper-writing/references/finance-prose-rubric.md",
    "skill/finance-paper-writing/references/multi-pass-adherence.md",
    "skill/finance-paper-writing/references/evidence-and-claims.md",
    "skill/finance-paper-writing/references/empirical-finance-section-jobs.md",
    "skill/finance-paper-writing/references/anti-defensive-prose.md",
    "skill/finance-paper-writing/references/closest-paper-positioning.md",
    "skill/finance-paper-writing/references/text-measure-papers.md",
    "skill/finance-paper-writing/scripts/init_run.py",
    "skill/finance-paper-writing/scripts/finance_prose_lint.py",
    "skill/finance-paper-writing/scripts/manuscript_hash.py",
    "skill/finance-paper-writing/scripts/validate_run_state.py",
    "skill/finance-paper-writing/templates/lint-dispositions.tsv",
    "scripts/install_local.py",
    "scripts/verify_local_install.py",
    "tests/test_finance_prose_lint.py",
    "tests/test_validate_run_state.py",
    "evals/rubric.md",
}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    missing = sorted(path for path in REQUIRED if not (root / path).is_file())
    errors.extend(f"missing required file: {path}" for path in missing)

    skill_files = sorted(root.rglob("SKILL.md"))
    canonical = root / "skill" / "finance-paper-writing" / "SKILL.md"
    if skill_files != [canonical]:
        errors.append(
            "repository must contain exactly one canonical SKILL.md; found: "
            + ", ".join(str(path.relative_to(root)) for path in skill_files)
        )

    if canonical.is_file():
        content = canonical.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]+\]\(((?!https?://)[^)]+)\)", content):
            relative = match.group(1).split("#")[0]
            if relative and not (canonical.parent / relative).exists():
                errors.append(f"broken SKILL.md link: {relative}")
        if "primary_capability: manuscript-prose" not in content:
            errors.append("SKILL.md does not declare manuscript prose as primary capability")
        if "text-measure-papers.md" not in content:
            errors.append("SKILL.md does not route the optional text-measure module")

    case_count = len(list((root / "evals" / "cases").glob("*.md")))
    if case_count < 5:
        errors.append(f"expected at least 5 regression cases, found {case_count}")
    result_count = len(list((root / "evals" / "results").glob("*.md")))
    if result_count < 1:
        errors.append("expected at least one documented evaluation result")

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    if "one pass, one job" not in readme.lower():
        errors.append("README does not explain pass separation")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"repository verification failed: {len(errors)} error(s)")
        return 1
    print("repository verification passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
