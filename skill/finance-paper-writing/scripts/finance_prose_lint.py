#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from manuscript_hash import manuscript_files, manuscript_sha256


TEXT_SUFFIXES = {".tex", ".md", ".txt"}
SKIP_DIRS = {".git", ".finance-writing", "build", "dist", "__pycache__"}


@dataclass
class Finding:
    severity: str
    category: str
    file: str
    line: int
    excerpt: str
    message: str
    finding_id: str = ""


PATTERNS: list[tuple[str, str, re.Pattern[str], str]] = [
    (
        "hard",
        "local-path",
        re.compile(r"(?:/Users/|/home/|file://|[A-Za-z]:\\Users\\|(?<!\w)~/)"),
        "Reader-facing prose appears to contain a local filesystem path.",
    ),
    (
        "warning",
        "awkward-author-role",
        re.compile(
            r"\b(?:human principal investigator|human researcher)\b",
            re.IGNORECASE,
        ),
        "Use ordinary author voice or a precise coding-role description.",
    ),
    (
        "warning",
        "development-record",
        re.compile(
            r"\b(?:locally archived|stored locally|on (?:my|the) computer|"
            r"generated manuscript exhibits|hash manifest|repair history|"
            r"superseded implementation|"
            r"no legacy (?:table|figure|exhibit|output) (?:is|was) used)\b",
            re.IGNORECASE,
        ),
        "Describe the data or method, not the project-development record.",
    ),
    (
        "hard",
        "internal-version-label",
        re.compile(
            r"\bv\d+(?:\.\d+)*(?:[- ](?:positive|negative|window|windows|"
            r"classifier|model|measure))\b",
            re.IGNORECASE,
        ),
        "Replace internal version labels with the economic rule or omit them.",
    ),
    (
        "warning",
        "internal-register",
        re.compile(
            r"\b(?:(?:Compustat|CRSP|DealScan|data|sample) backbone|"
            r"deployment model|model generation|"
            r"project governance|development pipeline)\b",
            re.IGNORECASE,
        ),
        "Check whether internal or software-oriented language can be translated into finance prose.",
    ),
    (
        "warning",
        "reviewer-directed",
        re.compile(
            r"\b(?:the appropriate test|reviewers? (?:may|might|could) "
            r"(?:worry|object|question)|to reassure reviewers?)\b",
            re.IGNORECASE,
        ),
        "State the economic test and evidence directly rather than addressing an imagined reviewer.",
    ),
    (
        "warning",
        "negative-contribution-framing",
        re.compile(
            r"\b(?:the contribution does not rest on|the question is not whether|"
            r"the comparison is not about|not whether)\b",
            re.IGNORECASE,
        ),
        "Open with the positive economic object or question rather than a negative contrast.",
    ),
    (
        "warning",
        "defensive-phrase",
        re.compile(
            r"\b(?:should not be interpreted as|should not be taken to mean|"
            r"we do not claim|we do not attempt|cannot establish|"
            r"need not (?:imply|display|be)|is not designed to|"
            r"this does not mean|this is not to say|the goal is not|"
            r"rather than arguing|association is not causation|"
            r"to be clear|it is worth noting)\b",
            re.IGNORECASE,
        ),
        "Check whether this qualification advances the argument, can be stated as positive scope, or belongs only once in its primary home.",
    ),
    (
        "warning",
        "negative-scope",
        re.compile(
            r"\b(?:we do not claim|we do not attempt|is not intended to|"
            r"is not designed to|the goal is not|should not be interpreted as)\b",
            re.IGNORECASE,
        ),
        "Consider stating the actual sample, estimand, design, horizon, comparison, or inferential scope positively without broadening the claim.",
    ),
    (
        "warning",
        "self-minimizing",
        re.compile(
            r"\b(?:merely|modest (?:attempt|contribution)|preliminary attempt|"
            r"only (?:a )?(?:small|limited|preliminary) (?:step|attempt|contribution))\b",
            re.IGNORECASE,
        ),
        "Replace ritual self-minimization with a precise statement of the paper's research job and supported contribution.",
    ),
]

MODULE_PATTERNS: dict[str, list[tuple[str, str, re.Pattern[str], str]]] = {
    "text-measure": [
        (
            "warning",
            "text-measure-internal-role",
            re.compile(
                r"\b(?:semantic teacher|student model|human labeler-in-the-loop)\b",
                re.IGNORECASE,
            ),
            "Use reader-facing descriptions of author guidance and classifier fidelity.",
        ),
        (
            "warning",
            "unqualified-label-truth",
            re.compile(r"\b(?:gold standard|ground truth)\b", re.IGNORECASE),
            "Confirm that the reference labels justify truth-oriented language.",
        ),
    ]
}

REPEATED_PHRASES = {
    "not-causal": re.compile(r"\b(?:not causal|noncausal|non-causal)\b", re.IGNORECASE),
    "cannot-establish": re.compile(r"\bcannot establish\b", re.IGNORECASE),
    "should-not-interpret": re.compile(r"\bshould not be interpreted\b", re.IGNORECASE),
    "do-not-claim": re.compile(r"\bwe do not claim\b", re.IGNORECASE),
}

NEGATIVE_OPENING = re.compile(
    r"^(?:although|while|despite|however|nevertheless)\b|"
    r"\b(?:cannot|need not|is not designed to|a limitation|a concern)\b",
    re.IGNORECASE,
)

HEDGE_MARKER = re.compile(
    r"\b(?:might|could|possibly|potentially|perhaps|arguably)\b",
    re.IGNORECASE,
)
LOWERCASE_MAY = re.compile(r"\bmay\b")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\\])")

HIGH_IMPACT_HEADING = re.compile(
    r"\b(?:abstract|introduction|contributions?|main results|empirical results|results|conclusion)\b",
    re.IGNORECASE,
)

HIGH_IMPACT_DEFENSE = re.compile(
    r"\b(?:we do not claim|we do not attempt|cannot establish|"
    r"should not be interpreted as|should not be taken to mean|"
    r"this does not mean|this is not to say|the goal is not|is not designed to)\b",
    re.IGNORECASE,
)

COMPLIANCE_HEADING = re.compile(
    r"(?:research ethics|use of artificial intelligence|author contributions|"
    r"funding|conflicts? of interest|reproducibility and governance)",
    re.IGNORECASE,
)


def source_files(
    target: Path,
    manuscript: Path | None = None,
    all_text: bool = False,
) -> list[Path]:
    if (
        manuscript
        and manuscript.is_file()
        and manuscript.suffix.lower() == ".tex"
        and not all_text
    ):
        return manuscript_files(manuscript)
    if target.is_file():
        return [target] if target.suffix.lower() in TEXT_SUFFIXES else []
    return sorted(
        path
        for path in target.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and not any(part in SKIP_DIRS for part in path.parts)
    )


def strip_tex_comment(line: str) -> str:
    result: list[str] = []
    escaped = False
    for char in line:
        if char == "%" and not escaped:
            break
        result.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    return "".join(result)


def is_nonprose_command(line: str) -> bool:
    stripped = line.strip()
    return bool(
        re.match(
            r"^\\(?:input|include|includegraphics|bibliography|addbibresource|"
            r"graphicspath|label|documentclass|usepackage)\b",
            stripped,
        )
    )


def normalized_prose(line: str, suffix: str) -> str:
    if suffix == ".tex":
        line = strip_tex_comment(line)
        if is_nonprose_command(line):
            return ""
        line = re.sub(r"\\(?:cite\w*|ref|autoref|label)\{[^}]*\}", " ", line)
        line = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", line)
        line = line.replace("{", " ").replace("}", " ")
    return re.sub(r"\s+", " ", line).strip()


def is_heading(raw: str, suffix: str) -> bool:
    stripped = raw.strip()
    if suffix == ".md":
        return stripped.startswith("#")
    if suffix == ".tex":
        return bool(re.match(r"^\\(?:part|chapter|section|subsection|subsubsection)\*?\{", stripped))
    return False


def heading_text(raw: str, suffix: str) -> str:
    if suffix == ".md":
        return raw.lstrip("#").strip()
    match = re.search(r"\{([^}]*)\}", raw)
    return match.group(1).strip() if match else raw.strip()


def heading_remainder(raw: str, suffix: str) -> str:
    if suffix != ".tex":
        return ""
    match = re.match(
        r"^\s*\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^}]*\}\s*(.*)$",
        strip_tex_comment(raw),
    )
    return match.group(1).strip() if match else ""


def hedge_count(text: str) -> int:
    return len(HEDGE_MARKER.findall(text)) + len(LOWERCASE_MAY.findall(text))


def sentence_units(prose_lines: list[str]) -> list[str]:
    corpus = " ".join(prose_lines)
    return [unit.strip() for unit in SENTENCE_SPLIT.split(corpus) if unit.strip()]


def lint_file(
    path: Path,
    active_patterns: list[tuple[str, str, re.Pattern[str], str]],
) -> tuple[list[Finding], str]:
    findings: list[Finding] = []
    all_prose: list[str] = []
    pending_heading: tuple[int, str] | None = None

    for line_number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        suffix = path.suffix.lower()
        if suffix == ".tex" and re.search(r"\\begin\{abstract\}", strip_tex_comment(raw)):
            pending_heading = (line_number, "Abstract")
            raw = re.sub(r".*?\\begin\{abstract\}\s*", "", raw, count=1)
            if not raw.strip():
                continue
        elif is_heading(raw, suffix):
            title = heading_text(raw, suffix)
            if COMPLIANCE_HEADING.search(title):
                findings.append(
                    Finding(
                        "warning",
                        "venue-check",
                        str(path),
                        line_number,
                        title[:180],
                        "Confirm that this compliance section is required or materially informative.",
                    )
                )
            pending_heading = (line_number, title)
            raw = heading_remainder(raw, suffix)
            if not raw:
                continue

        raw_prose = strip_tex_comment(raw) if suffix == ".tex" else raw
        for severity, category, pattern, message in active_patterns:
            if category == "local-path" and pattern.search(raw_prose):
                findings.append(
                    Finding(severity, category, str(path), line_number, raw_prose.strip()[:180], message)
                )

        prose = normalized_prose(raw, suffix)
        if not prose:
            continue
        all_prose.append(prose)

        if pending_heading is not None:
            if NEGATIVE_OPENING.search(prose):
                findings.append(
                    Finding(
                        "warning",
                        "negative-section-opening",
                        str(path),
                        line_number,
                        prose[:180],
                        f"Section '{pending_heading[1]}' appears to open with a caveat or defense.",
                    )
                )
            if HIGH_IMPACT_HEADING.search(pending_heading[1]) and (
                HIGH_IMPACT_DEFENSE.search(prose)
                or hedge_count(prose) >= 2
            ):
                findings.append(
                    Finding(
                        "warning",
                        "high-impact-defense",
                        str(path),
                        line_number,
                        prose[:180],
                        f"High-impact section '{pending_heading[1]}' opens with defensive framing or stacked uncertainty.",
                    )
                )
            pending_heading = None

        for severity, category, pattern, message in active_patterns:
            if category == "local-path":
                continue
            if pattern.search(prose):
                findings.append(
                    Finding(severity, category, str(path), line_number, prose[:180], message)
                )

    for sentence in sentence_units(all_prose):
        if hedge_count(sentence) >= 2:
            findings.append(
                Finding(
                    "warning",
                    "hedge-stack",
                    str(path),
                    0,
                    sentence[:180],
                    "This sentence stacks uncertainty markers; identify the concrete source of uncertainty and state it once.",
                )
            )

        negations = re.findall(
            r"\b(?:not|cannot|does not|do not|need not|should not)\b",
            sentence,
            flags=re.IGNORECASE,
        )
        if len(negations) >= 3:
            findings.append(
                Finding(
                    "warning",
                    "negation-chain",
                    str(path),
                    0,
                    sentence[:180],
                    "This sentence contains a chain of denials; reconstruct it around the supported claim.",
                )
            )

    return findings, "\n".join(all_prose)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Flag recurring finance-manuscript prose failures.")
    parser.add_argument("target", type=Path)
    parser.add_argument("--manuscript", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument(
        "--all-text",
        action="store_true",
        help="Scan every supported text file under a directory instead of the TeX dependency tree.",
    )
    parser.add_argument(
        "--module",
        action="append",
        choices=sorted(MODULE_PATTERNS),
        default=[],
        help="Enable an optional design-specific lint module.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target.expanduser().resolve()
    if not target.exists():
        raise SystemExit(f"target not found: {target}")

    manuscript = (
        args.manuscript.expanduser().resolve()
        if args.manuscript
        else (target if target.is_file() else None)
    )
    files = source_files(target, manuscript=manuscript, all_text=args.all_text)
    if not files:
        raise SystemExit("no .tex, .md, or .txt files found")

    findings: list[Finding] = []
    corpus_parts: list[str] = []
    active_patterns = list(PATTERNS)
    for module in args.module:
        active_patterns.extend(MODULE_PATTERNS[module])
    for path in files:
        file_findings, prose = lint_file(path, active_patterns)
        findings.extend(file_findings)
        corpus_parts.append(prose)

    corpus = "\n".join(corpus_parts)
    for label, pattern in REPEATED_PHRASES.items():
        count = len(pattern.findall(corpus))
        if count > 1:
            findings.append(
                Finding(
                    "warning",
                    "repeated-disclaimer",
                    str(target),
                    0,
                    f"{label}: {count} occurrences",
                    "Consolidate repeated claim-boundary language into its primary manuscript location.",
                )
            )

    for item in findings:
        identity = "|".join(
            (item.category, item.file, str(item.line), item.excerpt)
        )
        item.finding_id = "fpw-" + hashlib.sha256(
            identity.encode("utf-8")
        ).hexdigest()[:12]

    manuscript_hash = (
        manuscript_sha256(manuscript) if manuscript and manuscript.is_file() else ""
    )
    hard_count = sum(item.severity == "hard" for item in findings)
    warning_count = sum(item.severity == "warning" for item in findings)

    result = {
        "target": str(target),
        "files_scanned": [str(path) for path in files],
        "manuscript": str(manuscript) if manuscript else "",
        "manuscript_sha256": manuscript_hash,
        "hard_failure_count": hard_count,
        "warning_count": warning_count,
        "modules": sorted(set(args.module)),
        "findings": [asdict(item) for item in findings],
    }

    if args.json_output:
        output = args.json_output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    for item in findings:
        location = f"{item.file}:{item.line}" if item.line else item.file
        print(f"{item.severity.upper()} [{item.category}] {location}")
        print(f"  {item.message}")
        if item.excerpt:
            print(f"  {item.excerpt}")
    print(f"summary: {hard_count} hard, {warning_count} warning")

    if hard_count or (args.strict and warning_count):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
