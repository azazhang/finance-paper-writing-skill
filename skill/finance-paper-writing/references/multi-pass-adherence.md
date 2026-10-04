# Multi-Pass Adherence Protocol

This protocol exists because installed writing guidance can fail in two ways: it may not trigger, or the active agent may collapse it into an informal self-review. Make compliance visible and testable.

## Activation

At the start of a manuscript-level task:

1. state that `finance-paper-writing` is active;
2. choose a mode;
3. initialize a run directory;
4. record the skill version and manuscript hash; and
5. identify the lead editor.

Do not assume that another academic-writing or proofreading skill supplies these gates.

## Required Run Artifacts

| Artifact | Purpose |
|---|---|
| `run.json` | Scope, mode, manuscript, skill version, composite hashes, selected edit passes, roles, and gate status |
| `paper-charter.md` | Economic question, reader importance, headline, contribution, and claim ceiling |
| `claim-evidence-ledger.csv` | Trace manuscript claims to current evidence |
| `section-story-map.md` | Section jobs, decisive evidence, transitions, and caveat homes |
| `caveat-registry.csv` | One primary home and disposition for each material limitation in the affected scope |
| `macro-prose-audit.md` | Section jobs, argument order, evidence emphasis, and caveat placement |
| `issue-ledger.tsv` | Material prose and architecture issues with origin/reviewer classification, resolution evidence, and status |
| `pass-log.tsv` | Distinct pass purpose, role, identity, hashes, artifact, issues opened and closed, and status |
| `cold-reader-report.md` | Context-isolated reading of the final paper |
| `completion-report.md` | Gate results, accepted limitations, and unverified items |
| `prose-lint.json` | Deterministic linter results tied to a manuscript hash |
| `lint-dispositions.tsv` | Resolution or reasoned acceptance of each stable linter finding |

Full manuscripts use all artifacts. Section revisions use the same caveat registry but limit it to material limitations affected by the section revision; they do not inventory unrelated whole-paper caveats. Read-only audits use the charter excerpt, macro audit, issue and pass logs, linter output, and dispositions. These artifacts are internal. Never copy their vocabulary into the manuscript merely because it is available.

## Role Separation

| Role | May edit? | Context |
|---|---:|---|
| Lead finance writer | Yes | Manuscript, current evidence, author feedback |
| Prose referee | No | Manuscript plus finance-prose rubric |
| Cold finance reader | No | Final manuscript or skimming bundle only |
| Evidence auditor | No | Manuscript, exhibits, and claim ledger |

For a full manuscript, the lead writer cannot serve as either the `cold-reader` or the `final-whole-paper-read` acceptance reader. Record identities in `pass-log.tsv`; the two reads may use the same independent reader when appropriate, but both must be read-only and hash-current.

If independent agents are unavailable, start an isolated-context review and label it `lower-assurance`. Do not call it independent.

## Reviewer-to-Manuscript Firewall

Independent review expands the set of possible objections. It must not automatically expand the manuscript's caveats.

Classify every material issue before editing. Use `editor-detected` for issues found by the lead writer or deterministic checks; classify review-generated issues as follows:

| Review class | Meaning | Default action |
|---|---|---|
| `editor-detected` | The lead editor or deterministic checks identified the issue outside an independent review comment | Repair or disposition it under the ordinary issue workflow |
| `demonstrated-defect` | The manuscript or current evidence already shows a real problem | Repair the underlying claim, evidence order, design explanation, scope, or prose |
| `verification-question` | The concern might be real but requires checking | Verify first; edit only if the concern is confirmed or clarification is genuinely needed |
| `optional-extension` | Additional analysis or discussion that is not necessary to sustain the current claim | Keep outside the manuscript unless the author elects to expand the paper |

A review-generated issue must record the reviewer identity. A closed review-generated issue must record a short `review_resolution`; for a verification question, that resolution must state what evidence or check established whether the concern was real. Do not convert `verification-question` or `optional-extension` comments into defensive limitations merely to preempt a hypothetical referee. When a concern is accepted, prefer repairing the underlying source of ambiguity or overclaiming to appending a sentence such as `we do not claim...`.

If a review comment identifies a material limitation that was missing, add it to the caveat registry with its function, disposition, primary home, and calibrated wording before revising the manuscript.

## One Pass, One Job

Every pass record must contain:

- one named objective;
- role and identity;
- input manuscript SHA-256;
- output manuscript SHA-256 when editing;
- produced report or artifact;
- status; and
- issues opened or closed.

Do not combine economic architecture, sentence polishing, evidence checking, and final approval in one pass record.

## Freshness

An acceptance review applies only to the composite hash of the main manuscript and its recursively included TeX sources. Any later edit to that source tree makes the review stale.

Before completion:

1. compute the current manuscript hash;
2. verify the cold-reader and evidence-audit records use that hash;
3. rerun the prose linter on that hash;
4. compile and inspect the same source state; and
5. set `final_manuscript_sha256` in `run.json`.

## Issue Closure

An issue may close only when:

- the relevant manuscript passage or architecture changed;
- the affected full section was reread;
- the issue ledger records the repair; and
- no new material issue of the same category appears elsewhere in the affected scope.

Replacing a flagged word is not sufficient when the paragraph’s function remains defensive or unclear.

## Completion Enforcement

`validate_run_state.py` checks:

- required artifacts;
- final manuscript hash;
- linter freshness and hard failures;
- unresolved critical or major issues;
- distinct passes;
- coherent edit-pass hash chains and existing artifacts;
- reviewer independence;
- current-hash cold-reader and evidence checks; and
- the embedded finance-prose scorecard and critical-failure test;
- manual gate statuses.

The validator cannot judge persuasiveness. A passing script is necessary but not sufficient.

## Stopping Rule

For a full manuscript, stop when:

- no unresolved material issue remains;
- the final-hash `cold-reader` pass and the subsequent `final-whole-paper-read` form two consecutive acceptance reads and add only copy-level comments;
- all acceptance checks apply to the final hash; and
- further edits would reflect taste rather than a logged reader problem.

For a section revision, stop when a hash-current cold read finds no major issue in the affected section, the surrounding transitions still work, and all changed claims pass evidence checks. Do not impose a second whole-paper convergence cycle unless the edit changes the paper-level story.

For a read-only prose audit, stop after the macro and focused audit passes produce a complete severity-ranked issue ledger and current linter dispositions.

If structural objections persist, return to the economic story, evidence order, or research design. Do not continue aesthetic rewriting indefinitely.
