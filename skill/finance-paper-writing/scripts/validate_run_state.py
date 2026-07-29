#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from manuscript_hash import manuscript_sha256


COMMON_FILES = {
    "run.json",
    "paper-charter.md",
    "macro-prose-audit.md",
    "issue-ledger.tsv",
    "pass-log.tsv",
    "prose-lint.json",
    "lint-dispositions.tsv",
}
FILES_BY_MODE = {
    "full-manuscript": COMMON_FILES
    | {
        "claim-evidence-ledger.csv",
        "section-story-map.md",
        "caveat-registry.csv",
        "cold-reader-report.md",
        "completion-report.md",
    },
    "section-revision": COMMON_FILES
    | {
        "claim-evidence-ledger.csv",
        "section-story-map.md",
        "cold-reader-report.md",
        "completion-report.md",
    },
    "prose-audit": COMMON_FILES,
}

EDITING_PURPOSES = (
    "economics-rewrite",
    "evidence-prominence",
    "development-translation",
    "anti-defense",
    "reader-context",
    "finance-register",
    "closest-paper-positioning",
    "continuity",
)
MINIMUM_SECTION_EDIT_PASSES = {
    "economics-rewrite",
    "anti-defense",
    "reader-context",
    "finance-register",
    "continuity",
}
AUDIT_PURPOSES = {
    "macro-prose-audit",
    "development-language-audit",
    "anti-defense-audit",
    "reader-context-audit",
    "finance-register-audit",
}
ROLE_BY_PURPOSE = {
    "story-contract": "lead_writer",
    "macro-prose-audit": "prose_referee",
    "economics-rewrite": "lead_writer",
    "evidence-prominence": "lead_writer",
    "development-translation": "lead_writer",
    "anti-defense": "lead_writer",
    "reader-context": "lead_writer",
    "finance-register": "lead_writer",
    "closest-paper-positioning": "lead_writer",
    "continuity": "lead_writer",
    "development-language-audit": "prose_referee",
    "anti-defense-audit": "prose_referee",
    "reader-context-audit": "prose_referee",
    "finance-register-audit": "prose_referee",
    "cold-reader": "cold_reader",
    "evidence-audit": "evidence_auditor",
    "final-whole-paper-read": "cold_reader",
}

PASS_VALUES = {"pass", "passed", "complete", "completed"}
CLOSED_VALUES = {"closed", "resolved", "fixed"}
NOT_APPLICABLE = {"not-applicable", "not_applicable", "n/a"}
DISPOSITION_VALUES = {"resolved", "accepted-with-reason"}
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
GATES_BY_MODE = {
    "full-manuscript": {
        "evidence_boundary",
        "macro_prose",
        "finance_register",
        "cold_reader",
        "evidence_integrity",
        "rendered_paper",
        "convergence",
    },
    "section-revision": {
        "evidence_boundary",
        "macro_prose",
        "finance_register",
        "cold_reader",
        "evidence_integrity",
    },
    "prose-audit": {
        "macro_prose",
        "finance_register",
    },
}
SCORE_DIMENSIONS = (
    "economic_question",
    "result_led_exposition",
    "finance_register",
    "evidence_prominence",
    "caveat_discipline",
    "reader_context",
    "closest_paper_positioning",
    "claim_calibration",
)
GATE_LABELS = {
    "evidence boundary": "evidence_boundary",
    "macro prose": "macro_prose",
    "finance register": "finance_register",
    "independent cold reader": "cold_reader",
    "evidence integrity": "evidence_integrity",
    "rendered paper": "rendered_paper",
    "convergence": "convergence",
}
KNOWN_MODULES = {"text-measure"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def substantive_word_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [
        line
        for line in text.splitlines()
        if line.strip()
        and not line.lstrip().startswith(("#", "|", "<!--"))
    ]
    return len(" ".join(lines).split())


def valid_hash(value: str) -> bool:
    return bool(HASH_PATTERN.fullmatch(value.strip()))


def parse_scorecard(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    start_marker = "<!-- finance-writing-scorecard:start -->"
    end_marker = "<!-- finance-writing-scorecard:end -->"
    if start_marker not in text or end_marker not in text:
        return {}
    block = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
    values: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def parse_completion_gates(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        key = GATE_LABELS.get(cells[0].lower())
        if key:
            values[key] = cells[1].lower()
    return values


def required_purposes(mode: str, edit_passes: list[str]) -> list[str]:
    if mode == "full-manuscript":
        return [
            "story-contract",
            "macro-prose-audit",
            *edit_passes,
            "cold-reader",
            "evidence-audit",
            "final-whole-paper-read",
        ]
    if mode == "section-revision":
        return [
            "story-contract",
            "macro-prose-audit",
            *edit_passes,
            "cold-reader",
            "evidence-audit",
        ]
    return [
        "macro-prose-audit",
        "development-language-audit",
        "anti-defense-audit",
        "reader-context-audit",
        "finance-register-audit",
    ]


def validate_scorecard(
    scorecard: dict[str, str],
    mode: str,
    current_hash: str,
    cold_identity: str,
) -> list[str]:
    errors: list[str] = []
    if not scorecard:
        return ["cold reader scorecard is missing"]

    if scorecard.get("manuscript_sha256") != current_hash:
        errors.append("cold reader scorecard hash is stale")
    if scorecard.get("reviewer_identity") != cold_identity:
        errors.append("cold reader scorecard identity does not match pass log")

    total = 0
    applicable = 0
    for dimension in SCORE_DIMENSIONS:
        raw_score = scorecard.get(f"{dimension}_score", "").lower()
        evidence = scorecard.get(f"{dimension}_evidence", "").strip()
        if raw_score in NOT_APPLICABLE:
            if mode == "full-manuscript":
                errors.append(f"full manuscript score cannot omit: {dimension}")
            continue
        try:
            score = int(raw_score)
        except ValueError:
            errors.append(f"invalid score for {dimension}: {raw_score!r}")
            continue
        if score not in {0, 1, 2}:
            errors.append(f"score out of range for {dimension}: {score}")
            continue
        if len(evidence.split()) < 3:
            errors.append(f"score lacks evidence for {dimension}")
        total += score
        applicable += 1

    minimum_dimensions = 8 if mode == "full-manuscript" else 5
    if applicable < minimum_dimensions:
        errors.append(
            f"too few applicable prose dimensions: {applicable} < {minimum_dimensions}"
        )
    try:
        declared_dimensions = int(scorecard.get("applicable_dimensions", ""))
    except ValueError:
        declared_dimensions = -1
    if declared_dimensions != applicable:
        errors.append("applicable_dimensions does not match scored dimensions")
    try:
        declared_total = int(scorecard.get("total_score", ""))
    except ValueError:
        declared_total = -1
    if declared_total != total:
        errors.append("total_score does not match dimension scores")
    if applicable and total / (2 * applicable) < 0.875:
        errors.append(
            f"cold reader score below threshold: {total}/{2 * applicable}"
        )
    if scorecard.get("critical_failure", "").lower() not in {"false", "no"}:
        errors.append("cold reader reports or leaves open a critical failure")
    if scorecard.get("decision", "").lower() not in {"pass", "passed", "accept"}:
        errors.append("cold reader decision is not pass")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a finance-paper-writing run.")
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("--allow-lower-assurance", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_directory.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not run_dir.is_dir():
        raise SystemExit(f"run directory not found: {run_dir}")
    if not (run_dir / "run.json").is_file():
        raise SystemExit(f"run.json not found: {run_dir}")

    run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    mode = run.get("mode", "")
    if mode not in FILES_BY_MODE:
        errors.append(f"unknown run mode: {mode}")
        mode = "full-manuscript"

    missing = sorted(
        name for name in FILES_BY_MODE[mode] if not (run_dir / name).is_file()
    )
    errors.extend(f"missing required artifact: {name}" for name in missing)
    if missing:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    manuscript = Path(run.get("manuscript", "")).expanduser()
    if not manuscript.is_file():
        errors.append(f"manuscript not found: {manuscript}")
        current_hash = ""
    else:
        current_hash = manuscript_sha256(manuscript)

    baseline_hash = str(run.get("baseline_manuscript_sha256", ""))
    final_hash = str(run.get("final_manuscript_sha256", ""))
    if not valid_hash(baseline_hash):
        errors.append("baseline_manuscript_sha256 is invalid")
    if not valid_hash(final_hash):
        errors.append("final_manuscript_sha256 is invalid")
    elif current_hash and final_hash != current_hash:
        errors.append("final manuscript hash is stale")
    if (
        mode in {"full-manuscript", "section-revision"}
        and current_hash
        and baseline_hash == current_hash
    ):
        errors.append(
            "editing mode contains no manuscript state change; use prose-audit for a no-change outcome"
        )

    lead_editor = run.get("lead_editor", "").strip()
    if not lead_editor:
        errors.append("lead_editor is empty")

    edit_passes = run.get("required_edit_passes", [])
    if not isinstance(edit_passes, list):
        errors.append("required_edit_passes must be a list")
        edit_passes = []
    if len(edit_passes) != len(set(edit_passes)):
        errors.append("required_edit_passes contains duplicates")
    unknown_edit_passes = set(edit_passes) - set(EDITING_PURPOSES)
    if unknown_edit_passes:
        errors.append(
            "unknown required edit pass(es): "
            + ", ".join(sorted(unknown_edit_passes))
        )
    if mode == "full-manuscript" and set(edit_passes) != set(EDITING_PURPOSES):
        errors.append("full-manuscript mode must retain all eight edit passes")
    if mode == "section-revision" and not MINIMUM_SECTION_EDIT_PASSES.issubset(
        edit_passes
    ):
        errors.append("section-revision mode omits a mandatory core prose pass")
    if mode == "prose-audit" and edit_passes:
        errors.append("prose-audit mode cannot require editing passes")

    optional_modules = run.get("optional_modules", [])
    if not isinstance(optional_modules, list):
        errors.append("optional_modules must be a list")
        optional_modules = []
    unknown_modules = set(optional_modules) - KNOWN_MODULES
    if unknown_modules:
        errors.append(
            "unknown optional module(s): " + ", ".join(sorted(unknown_modules))
        )

    gates = run.get("gates", {})
    required_gates = GATES_BY_MODE[mode]
    for gate in sorted(required_gates - gates.keys()):
        errors.append(f"required gate missing: {gate}")
    for gate, status in gates.items():
        normalized = str(status).lower()
        if gate in required_gates and normalized not in PASS_VALUES:
            errors.append(f"gate not passed: {gate}={status}")
        elif gate not in required_gates and normalized not in PASS_VALUES | NOT_APPLICABLE:
            errors.append(f"gate has invalid status: {gate}={status}")

    lint = json.loads((run_dir / "prose-lint.json").read_text(encoding="utf-8"))
    if current_hash and lint.get("manuscript_sha256") != current_hash:
        errors.append("prose linter result is stale")
    if lint.get("hard_failure_count", 0):
        errors.append(f"prose linter has {lint['hard_failure_count']} hard failure(s)")
    if sorted(set(lint.get("modules", []))) != sorted(set(optional_modules)):
        errors.append("prose linter modules do not match run.json")

    dispositions = {
        row.get("finding_id", "").strip(): row
        for row in read_tsv(run_dir / "lint-dispositions.tsv")
        if row.get("finding_id", "").strip()
    }
    for finding in lint.get("findings", []):
        finding_id = finding.get("finding_id", "")
        disposition = dispositions.get(finding_id)
        if not finding_id:
            errors.append("linter finding has no stable finding_id")
            continue
        if not disposition:
            errors.append(f"linter finding has no disposition: {finding_id}")
            continue
        value = disposition.get("disposition", "").strip().lower()
        if value not in DISPOSITION_VALUES:
            errors.append(f"invalid lint disposition for {finding_id}: {value}")
        if finding.get("severity") == "hard" and value != "resolved":
            errors.append(f"hard lint finding not resolved: {finding_id}")
        if value == "accepted-with-reason" and len(
            disposition.get("reason", "").split()
        ) < 3:
            errors.append(f"accepted lint finding lacks reason: {finding_id}")

    issues = read_tsv(run_dir / "issue-ledger.tsv")
    for issue in issues:
        severity = issue.get("severity", "").strip().lower()
        status = issue.get("status", "").strip().lower()
        if severity in {"critical", "major"} and status not in CLOSED_VALUES:
            errors.append(
                f"unresolved {severity} issue: {issue.get('issue_id', '')} "
                f"{issue.get('description', '')}".strip()
            )

    passes = read_tsv(run_dir / "pass-log.tsv")
    pass_ids: set[str] = set()
    completed: dict[str, dict[str, str]] = {}
    for row in passes:
        pass_id = row.get("pass_id", "").strip()
        purpose = row.get("purpose", "").strip()
        status = row.get("status", "").strip().lower()
        if not pass_id or pass_id in pass_ids:
            errors.append(f"blank or duplicate pass_id: {pass_id!r}")
        pass_ids.add(pass_id)
        if purpose not in ROLE_BY_PURPOSE:
            errors.append(f"unknown pass purpose: {purpose}")
            continue
        if status not in PASS_VALUES:
            errors.append(f"pass not completed: {purpose}={status}")
            continue
        if purpose in completed:
            errors.append(f"duplicate completed pass purpose: {purpose}")
            continue
        completed[purpose] = row
        expected_role = ROLE_BY_PURPOSE[purpose]
        if row.get("role", "").strip() != expected_role:
            errors.append(f"incorrect role for {purpose}: expected {expected_role}")
        identity = row.get("identity", "").strip()
        if not identity:
            errors.append(f"identity missing for pass: {purpose}")
        input_hash = row.get("input_sha256", "").strip()
        if not valid_hash(input_hash):
            errors.append(f"invalid input hash for pass: {purpose}")
        output_hash = row.get("output_sha256", "").strip()
        if purpose in EDITING_PURPOSES and not valid_hash(output_hash):
            errors.append(f"invalid output hash for edit pass: {purpose}")
        artifact = row.get("artifact", "").strip()
        if not artifact:
            errors.append(f"artifact missing for pass: {purpose}")
        elif artifact != "manuscript" and not (run_dir / artifact).is_file():
            errors.append(f"pass artifact does not exist: {purpose} -> {artifact}")

    required = required_purposes(mode, edit_passes)
    for purpose in required:
        if purpose not in completed:
            errors.append(f"required pass not completed: {purpose}")

    if mode in {"full-manuscript", "section-revision"}:
        for purpose in ("story-contract", "macro-prose-audit"):
            row = completed.get(purpose)
            if row and row.get("input_sha256", "").strip() != baseline_hash:
                errors.append(f"{purpose} did not inspect the baseline manuscript")

        prior_hash = baseline_hash
        for purpose in edit_passes:
            row = completed.get(purpose)
            if not row:
                continue
            if row.get("identity", "").strip() != lead_editor:
                errors.append(f"edit pass is not owned by lead editor: {purpose}")
            if row.get("input_sha256", "").strip() != prior_hash:
                errors.append(f"broken edit-pass hash chain at: {purpose}")
            prior_hash = row.get("output_sha256", "").strip()
        if current_hash and prior_hash != current_hash:
            errors.append("final edit-pass output does not match current manuscript")

        for purpose in ("cold-reader", "evidence-audit"):
            row = completed.get(purpose)
            if row and row.get("input_sha256", "").strip() != current_hash:
                errors.append(f"{purpose} review is stale")
        if mode == "full-manuscript":
            row = completed.get("final-whole-paper-read")
            if row and row.get("input_sha256", "").strip() != current_hash:
                errors.append("final-whole-paper-read review is stale")

        cold_row = completed.get("cold-reader", {})
        cold_identity = cold_row.get("identity", "").strip()
        if cold_identity == lead_editor:
            if run.get("assurance") == "lower-assurance" and args.allow_lower_assurance:
                warnings.append("cold reader is the lead editor; lower-assurance override used")
            else:
                errors.append("cold reader is not independent of the lead editor")
        evidence_identity = completed.get("evidence-audit", {}).get(
            "identity", ""
        ).strip()
        if evidence_identity == lead_editor:
            errors.append("evidence auditor is not independent of the lead editor")

        scorecard = parse_scorecard(run_dir / "cold-reader-report.md")
        errors.extend(
            validate_scorecard(scorecard, mode, current_hash, cold_identity)
        )

    if substantive_word_count(run_dir / "paper-charter.md") < (
        40 if mode != "prose-audit" else 20
    ):
        errors.append("paper charter is not substantively completed")
    if substantive_word_count(run_dir / "macro-prose-audit.md") < 40:
        errors.append("macro prose audit is not substantively completed")
    if mode in {"full-manuscript", "section-revision"}:
        if substantive_word_count(run_dir / "cold-reader-report.md") < 40:
            errors.append("cold reader report is not substantively completed")
        with (run_dir / "claim-evidence-ledger.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            if not list(csv.DictReader(handle)):
                errors.append("claim-evidence ledger has no affected claims")
        completion = (run_dir / "completion-report.md").read_text(
            encoding="utf-8", errors="replace"
        )
        if final_hash and final_hash not in completion:
            errors.append("completion report does not record the final manuscript hash")
        completion_gates = parse_completion_gates(
            run_dir / "completion-report.md"
        )
        for gate in gates:
            if gate not in completion_gates:
                errors.append(f"completion report omits gate: {gate}")
                continue
            reported = completion_gates[gate]
            if gate in required_gates and reported not in PASS_VALUES:
                errors.append(f"completion report gate not passed: {gate}")
            if gate not in required_gates and reported not in PASS_VALUES | NOT_APPLICABLE:
                errors.append(f"completion report gate has invalid status: {gate}")
    else:
        for purpose in AUDIT_PURPOSES:
            row = completed.get(purpose)
            if row and row.get("input_sha256", "").strip() != current_hash:
                errors.append(f"prose audit pass is stale: {purpose}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"validation passed: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
