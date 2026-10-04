# Changelog

## 0.2.1 — 2026-10-04

- Hardened the evidence gate so manuscript-facing claims must be backed by current, verified evidence with an explicit inferential status and allowed verbs.
- Required affected-scope caveat tracking in section revisions and prevented material scope or evidence qualifications from being deleted as noninformative.
- Required issue origin/reviewer classification and resolution evidence for closed review-generated concerns.
- Enforced read-only prose-audit mode and rejected unsupported run-artifact schema versions.
- Made hedge-stack checks sentence-based, fixed line-wrapping and month-name false positives, recognized abstract and inline section openings, and improved Windows-path detection.
- Demoted ambiguous development-record wording such as `stored locally` from a hard failure to a judgment-required warning.
- Added the portable `~/.agents/skills` installation target and protected managed-copy local edits from forced replacement unless explicitly discarded.
- Expanded regression coverage for the independent-review failures found during the v0.2.0 audit.

## 0.2.0 — 2026-10-04

- Added functional classification of defensive prose before rewriting.
- Added positive-scope conversion for negative claim boundaries without relaxing inferential limits.
- Added calibrated hedge-stack detection and high-impact-position warnings.
- Added reviewer-to-manuscript triage: demonstrated defects, verification questions, and optional extensions.
- Added evidence-first treatment of null, mixed, and unfavorable results.
- Extended caveat and issue ledgers with disposition and review-class fields.
- Introduced run-artifact schema v2 while preserving validation compatibility for existing schema-v1 runs.
- Added run-state validation preventing deletion of real methodological limitations as noninformative.
- Added five anti-defense regression cases and new linter/validator unit tests.

## 0.1.0 — 2026-07-28

- Added the canonical `finance-paper-writing` skill.
- Added a prose-first empirical-finance workflow with recorded gates.
- Added independent-review and manuscript-hash freshness requirements.
- Added a deterministic prose linter and run-state validator.
- Added a text-measure extension as an optional module.
- Added generalized evaluation cases and unit tests.
- Added safe local installation for Codex, Claude Code, and Cursor.

