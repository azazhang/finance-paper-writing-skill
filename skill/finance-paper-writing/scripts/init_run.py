#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from manuscript_hash import manuscript_sha256


MODES = ("full-manuscript", "section-revision", "prose-audit")
MODULES = ("text-measure",)

TEMPLATES_BY_MODE = {
    "full-manuscript": {
        "paper-charter.md",
        "claim-evidence-ledger.csv",
        "section-story-map.md",
        "caveat-registry.csv",
        "macro-prose-audit.md",
        "issue-ledger.tsv",
        "pass-log.tsv",
        "cold-reader-report.md",
        "completion-report.md",
        "lint-dispositions.tsv",
    },
    "section-revision": {
        "paper-charter.md",
        "claim-evidence-ledger.csv",
        "section-story-map.md",
        "caveat-registry.csv",
        "macro-prose-audit.md",
        "issue-ledger.tsv",
        "pass-log.tsv",
        "cold-reader-report.md",
        "completion-report.md",
        "lint-dispositions.tsv",
    },
    "prose-audit": {
        "paper-charter.md",
        "macro-prose-audit.md",
        "issue-ledger.tsv",
        "pass-log.tsv",
        "lint-dispositions.tsv",
    },
}

PASS_DEFINITIONS = {
    "story-contract": ("lead_writer", "paper-charter.md"),
    "macro-prose-audit": ("prose_referee", "macro-prose-audit.md"),
    "economics-rewrite": ("lead_writer", "manuscript"),
    "evidence-prominence": ("lead_writer", "manuscript"),
    "development-translation": ("lead_writer", "manuscript"),
    "anti-defense": ("lead_writer", "manuscript"),
    "reader-context": ("lead_writer", "manuscript"),
    "finance-register": ("lead_writer", "manuscript"),
    "closest-paper-positioning": ("lead_writer", "manuscript"),
    "continuity": ("lead_writer", "manuscript"),
    "development-language-audit": ("prose_referee", "issue-ledger.tsv"),
    "anti-defense-audit": ("prose_referee", "issue-ledger.tsv"),
    "reader-context-audit": ("prose_referee", "issue-ledger.tsv"),
    "finance-register-audit": ("prose_referee", "issue-ledger.tsv"),
    "cold-reader": ("cold_reader", "cold-reader-report.md"),
    "evidence-audit": ("evidence_auditor", "claim-evidence-ledger.csv"),
    "final-whole-paper-read": ("cold_reader", "completion-report.md"),
}

EDIT_PASSES_BY_MODE = {
    "full-manuscript": [
        "economics-rewrite",
        "evidence-prominence",
        "development-translation",
        "anti-defense",
        "reader-context",
        "finance-register",
        "closest-paper-positioning",
        "continuity",
    ],
    "section-revision": [
        "economics-rewrite",
        "evidence-prominence",
        "development-translation",
        "anti-defense",
        "reader-context",
        "finance-register",
        "continuity",
    ],
    "prose-audit": [],
}

PASSES_BY_MODE = {
    "full-manuscript": [
        "story-contract",
        "macro-prose-audit",
        *EDIT_PASSES_BY_MODE["full-manuscript"],
        "cold-reader",
        "evidence-audit",
        "final-whole-paper-read",
    ],
    "section-revision": [
        "story-contract",
        "macro-prose-audit",
        *EDIT_PASSES_BY_MODE["section-revision"],
        "cold-reader",
        "evidence-audit",
    ],
    "prose-audit": [
        "macro-prose-audit",
        "development-language-audit",
        "anti-defense-audit",
        "reader-context-audit",
        "finance-register-audit",
    ],
}


def find_project_root(path: Path) -> Path:
    for candidate in (path.parent, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return path.parent


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "manuscript"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a finance-paper-writing run.")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--mode", choices=MODES, default="full-manuscript")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--slug")
    parser.add_argument("--lead-editor", default="")
    parser.add_argument("--venue", default="")
    parser.add_argument("--author-convention", default="")
    parser.add_argument("--scope", default="")
    parser.add_argument(
        "--module",
        action="append",
        choices=MODULES,
        default=[],
        help="Record an optional design-specific module. Repeat when needed.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manuscript = args.manuscript.expanduser().resolve()
    if not manuscript.is_file():
        raise SystemExit(f"manuscript not found: {manuscript}")

    project_root = (
        args.project_root.expanduser().resolve()
        if args.project_root
        else find_project_root(manuscript)
    )
    if not project_root.is_dir():
        raise SystemExit(f"project root not found: {project_root}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    slug = slugify(args.slug or manuscript.stem)
    run_dir = project_root / ".finance-writing" / "runs" / f"{stamp}-{slug}"
    if run_dir.exists():
        raise SystemExit(f"run directory already exists: {run_dir}")
    run_dir.mkdir(parents=True)

    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "templates"
    for source in sorted(templates.iterdir()):
        if source.is_file() and source.name in TEMPLATES_BY_MODE[args.mode]:
            shutil.copy2(source, run_dir / source.name)

    with (run_dir / "pass-log.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(
            [
                "pass_id",
                "purpose",
                "role",
                "identity",
                "input_sha256",
                "output_sha256",
                "artifact",
                "issues_opened",
                "issues_closed",
                "status",
            ]
        )
        for index, purpose in enumerate(PASSES_BY_MODE[args.mode], 1):
            role, artifact = PASS_DEFINITIONS[purpose]
            writer.writerow(
                [
                    f"{index:02d}",
                    purpose,
                    role,
                    "",
                    "",
                    "",
                    artifact,
                    "",
                    "",
                    "pending",
                ]
            )

    run_data = json.loads((templates / "run.json").read_text(encoding="utf-8"))
    baseline = manuscript_sha256(manuscript)
    run_data.update(
        {
            "mode": args.mode,
            "scope": args.scope,
            "project_root": str(project_root),
            "manuscript": str(manuscript),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "lead_editor": args.lead_editor,
            "venue": args.venue,
            "author_convention": args.author_convention,
            "required_edit_passes": EDIT_PASSES_BY_MODE[args.mode],
            "optional_modules": sorted(set(args.module)),
            "baseline_manuscript_sha256": baseline,
        }
    )
    if args.mode == "prose-audit":
        run_data["final_manuscript_sha256"] = baseline
        for gate in (
            "evidence_boundary",
            "cold_reader",
            "evidence_integrity",
            "rendered_paper",
            "convergence",
        ):
            run_data["gates"][gate] = "not-applicable"
    elif args.mode == "section-revision":
        for gate in ("rendered_paper", "convergence"):
            run_data["gates"][gate] = "not-applicable"
    (run_dir / "run.json").write_text(
        json.dumps(run_data, indent=2) + "\n", encoding="utf-8"
    )

    print(run_dir)
    print(f"baseline_sha256={baseline}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
