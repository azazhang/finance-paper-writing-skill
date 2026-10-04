---
name: finance-paper-writing
description: "Draft and revise empirical finance manuscript prose through an economics-first, exhibit-linked, multi-pass workflow. Enforces finance-paper register, result-led argument, closest-paper positioning, caveat discipline, reader context, and independent whole-paper review. Use when writing or revising a finance paper, abstract, introduction, literature positioning, results narrative, or when prose sounds defensive, overly technical, generic, or like an internal development report. Not for literature discovery alone or generic proofreading."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(python3*)
  - Bash(latexmk*)
  - AskUserQuestion
  - Task
metadata:
  version: "0.2.1"
  domain: empirical-finance
  primary_capability: manuscript-prose
---

# Finance Paper Writing

Produce finance-facing manuscript prose, not a polished research log. Treat prose quality as a substantive part of the paper: the order of claims, evidence, qualifications, and comparisons determines what a finance reader believes the paper contributes.

## When to Use

Use this skill for:

- drafting or revising an empirical finance manuscript;
- rewriting an abstract, introduction, related-literature discussion, data section, or results narrative;
- removing defensive, generic, technical, or development-oriented prose;
- deciding what a main-text reader must see;
- conducting a first-principles finance-prose audit; or
- integrating completed evidence into a paper.

Do not use it as a substitute for:

- literature discovery: use a finance literature-review workflow;
- new empirical analysis or causal-design selection;
- mechanical proofreading alone;
- formal response-to-referee planning; or
- LaTeX compilation alone.

## Core Contract

For every manuscript-level task:

1. Announce that this skill is being used.
2. Select a mode and record it.
3. Create the required run artifacts before editing.
4. Complete distinct passes with one objective each.
5. Use at least one fresh read-only evaluator after substantive editing.
6. Report which gates passed and which did not.

Never claim that an installed companion skill ran unless it was actually invoked. Never declare a manuscript finished from an unrecorded self-review.

Read [multi-pass-adherence.md](references/multi-pass-adherence.md) for the enforcement protocol and [finance-prose-rubric.md](references/finance-prose-rubric.md) for the prose standard.

## Modes

| Mode | Use | Required artifacts |
|---|---|---|
| `full-manuscript` | New draft or whole-paper revision | Charter, affected-claim ledger, story map, caveat registry, audits, pass log, cold read, completion report |
| `section-revision` | An abstract, introduction, literature, data, results, or other substantive section | Charter excerpt, affected-claim ledger, section map, affected-caveat registry, audit, issue and pass logs, cold read |
| `prose-audit` | Diagnose without editing | Charter excerpt, macro-prose audit, issue and pass logs, lint dispositions |
| `paragraph-edit` | One isolated passage that does not change paper-level or section-level argument | Brief diagnosis and rewrite; no run directory required |

Use `section-revision`, not `paragraph-edit`, whenever the request names a manuscript section or requires contribution, evidence-order, closest-paper, or main-versus-Appendix judgment. Default to `full-manuscript` when the request concerns the paper’s overall contribution, main-text evidence, or several sections.

In `paragraph-edit` mode, still diagnose the paragraph’s economic job, remove repeated claim-boundary language, and apply the finance-prose rubric before returning the rewrite.

## Phase 0: Route and Inspect

Before editing:

1. Locate the active manuscript and rendered paper.
2. Identify the target venue and intended audience when available.
3. Separate current verified evidence from active development, legacy material, and provenance records.
4. Read prior author feedback and the nearest completed exhibits.
5. Select optional modules only when their trigger applies.

For `full-manuscript`, `section-revision`, and `prose-audit`, initialize:

```bash
python3 <skill-directory>/scripts/init_run.py <manuscript-file> --mode <mode>
```

This creates `.finance-writing/runs/<date>-<slug>/` in the project root. Keep these workflow artifacts out of the manuscript directory and out of reader-facing prose.

If an optional module applies, record it during initialization, for example `--module text-measure`. If a requested revision produces no manuscript change, convert the run to `prose-audit`; do not report a no-change audit as a completed revision.

Ask the author only when the economic question, intended contribution, or claim boundary cannot be inferred without a consequential assumption.

## Phase 1: Lock the Paper’s Economic Job

Complete the paper charter before polishing sentences. Record:

- economic question;
- why a finance reader should care;
- construct or treatment;
- unit of observation;
- research design and inferential status;
- strongest defensible finding;
- closest paper or construct;
- intended contribution;
- target reader promise; and
- material claim boundaries.

Then build the claim-evidence ledger for headline claims and for quantitative claims added or changed in the current scope. In a new full manuscript, cover every quantitative claim. Each row must map to current verified evidence, a sample and unit, an exhibit, an inferential status, and allowed verbs.

### Gate 1: Evidence Boundary

Do not draft a result as established when its ledger status is planned, provisional, failed, legacy, or unknown. Do not silently omit a material null merely because it complicates the preferred story.

Read [evidence-and-claims.md](references/evidence-and-claims.md).

## Phase 2: Build the Reader-Facing Architecture

Complete a section story map:

| Field | Required question |
|---|---|
| Reader question | Why does this section exist? |
| Section answer | What should the reader believe after it? |
| Decisive evidence | Which exhibit or citation earns that belief? |
| Interpretation | What is the economic meaning? |
| Transition | Why does the next section follow? |
| Caveat home | Which qualification belongs here, if any? |

Order the main exhibits before drafting long narrative. A reviewer who reads only the abstract, introduction, headings, main exhibits, and conclusion must encounter the strongest complete version of the argument.

Read [empirical-finance-section-jobs.md](references/empirical-finance-section-jobs.md).

### Gate 2: Architecture

Do not preserve a paragraph merely because it already exists. If its economic job is unclear, delete, combine, or rebuild it from a blank page.

## Phase 3: Draft or Rewrite in Distinct Passes

Use one pass for one job. Record each pass in `pass-log.tsv`.

| Pass | Objective | Do not change |
|---|---|---|
| Economics | Make the question, result, and interpretation explicit | Numbers or evidence status |
| Evidence prominence | Put claim-critical evidence where a skimming reader sees it | Estimates |
| Development translation | Replace project history with data, sample, and method descriptions | Reproducibility facts |
| Anti-defense | Diagnose defensive units, convert negative boundaries to positive scope when faithful, collapse hedge stacks, and prevent reviewer-objection leakage | Material limitations and claim ceilings |
| Reader context | Define samples, units, timing, groups, and acronyms at first use | Construct definitions |
| Finance register | Make syntax, author voice, and terminology natural for finance | Claim strength |
| Closest-paper positioning | Establish the neighboring economic object before differentiation | The cited paper’s actual contribution |
| Continuity | Repair headings, openings, transitions, and conclusion alignment | Evidence boundary |

`run.json` records `required_edit_passes`. Full-manuscript mode requires all eight. Section mode initializes the seven universal prose passes; after the macro audit, add `closest-paper-positioning` when the affected scope compares contributions or constructs. Do not replace several named passes with a catch-all rewrite.

Apply the paragraph order:

**economic point → evidence → interpretation → one bounded qualification when needed**

Do not force that sequence mechanically when a shorter paragraph is clearer.

During the anti-defense pass, classify each material defensive unit as an unnecessary disclaimer, redundant clarification, necessary scope condition, real methodological limitation, evidence-based qualification, or useful conceptual contrast. Choose an explicit disposition before rewriting. Record every affected material limitation in `caveat-registry.csv`, scoped to the whole paper in full-manuscript mode and to the affected section in section-revision mode. Prefer positive statements of sample, estimand, design, horizon, comparison, or inferential status to negative self-protection when they preserve the same boundary. Do not remove a qualification if doing so broadens the claim beyond the evidence.

Treat null, mixed, or unfavorable evidence as evidence first. State the condition and finding directly, then narrow or withdraw the affected claim when required. Do not convert adverse evidence into generic self-criticism or hide it behind a limitations label.

Read [anti-defensive-prose.md](references/anti-defensive-prose.md) and [closest-paper-positioning.md](references/closest-paper-positioning.md).

## Phase 4: Run the Prose Enforcement Checks

Run:

```bash
python3 <skill-directory>/scripts/finance_prose_lint.py <manuscript-source> \
  --manuscript <main-manuscript-file> \
  --json-output <run-directory>/prose-lint.json
```

Treat its output as leads for judgment, not automatic edits. The linter detects recurring development language, reviewer-directed prose, repeated disclaimers, awkward author roles, and local path leakage. It cannot decide whether the economic story works.

When the optional text-measure module applies, add `--module text-measure`.

Record every linter finding in `lint-dispositions.tsv` as `resolved` or `accepted-with-reason`. A final run may not retain a hard finding. Classify every material prose issue in `issue-ledger.tsv`. After local repairs, reread the full affected section; never close an issue based only on replacing the flagged phrase.

## Phase 5: Independent Finance-Reader Review

For `full-manuscript` and `section-revision`, use a fresh read-only agent that did not perform the immediately preceding edit. Give it the manuscript or rendered paper and the reader rubric, but withhold development notes unless needed to verify a specific claim. Record reviewer identity and the composite manuscript SHA-256 in `pass-log.tsv`.

Run at least:

1. **Skim test:** title, abstract, first two introduction pages, headings, main exhibits, conclusion.
2. **Finance-reader test:** importance, contribution, evidence order, interpretation, and prose credibility.
3. **Cold-context test:** undefined samples, timing, units, groups, acronyms, and unexplained comparisons.
4. **Forensic test:** numbers, signs, table references, citations, and claim verbs.

For a closest-paper discussion, add a fairness test: would the other paper’s authors recognize their contribution and the stated distinction?

Fresh agents report issues; one lead editor owns manuscript changes. Before any review comment becomes manuscript text, classify it as a **demonstrated defect**, **verification question**, or **optional extension**; classify non-reviewer issues as `editor-detected`. Demonstrated defects should be repaired. Verification questions must be checked before they are treated as problems, and a closed verification question must record what evidence resolved it. Optional extensions do not become caveats merely because a reviewer can imagine them; if the author elects to pursue one, record that decision rather than relabeling it as a defect. Repair accepted problems at the level of claim, evidence, design explanation, scope, or architecture rather than appending prophylactic language.

Complete the scorecard embedded in `cold-reader-report.md`. Full manuscripts must score all eight prose dimensions; section reviews may mark genuinely irrelevant dimensions `n/a`. Passing requires at least 87.5% of available points and no critical failure.

### Gate 3: Independent Review

Do not self-certify. If fresh review finds a recurring structural problem, return to the charter, exhibit order, or section job rather than applying another sentence-level patch.

## Phase 6: Integrity and Rendered-Paper Check

Cross-check:

- every prose number against its exhibit;
- sample sizes and units across text and tables;
- causal, predictive, and descriptive verbs against the design;
- all table, figure, section, and citation references;
- title, abstract, introduction, main exhibits, and conclusion for the same contribution; and
- the compiled PDF for table prominence, legibility, and awkward page-level flow.

Use companion skills for bibliography validation, formal proofreading, or PDF inspection when available. Record actual invocations in the pass log.

## Optional Modules

Load optional guidance only when applicable:

- For papers that construct or validate measures from text, classifiers, or LLM labels, read [text-measure-papers.md](references/text-measure-papers.md).
- For all other empirical finance papers, do not import classifier-validation terminology or requirements.

Optional modules may add checks. They may not replace the universal prose and evidence gates.

## Never Do These

- Do not convert an internal development report into a paper through word substitution alone.
- Do not lead a section with what the design cannot establish before stating what it does establish.
- Do not repeat “association is not causation” when calibrated verbs already communicate the boundary.
- Do not describe local files, version labels, hashes, model generations, repair history, or governance records as manuscript contributions.
- Do not allocate main-text space according to which analysis consumed the most development effort.
- Do not introduce a competing paper through rebuttal or overlap statistics before explaining its economic object.
- Do not insert ethics, AI-use, funding, authorship, limitations, or conflict sections unless the venue requires them or they materially inform the study.
- Do not call planned empirical work a result.
- Do not let the drafting agent serve as the only final reviewer.
- Do not turn hypothetical reviewer objections or optional extensions into manuscript caveats by default.
- Do not convert a necessary limitation into a stronger positive statement that the design cannot support.
- Do not relabel a material null or adverse result as a generic limitation to reduce its prominence.
- Do not use a prose linter as evidence that the manuscript is persuasive.

## Completion Gate

Validate the run state:

```bash
python3 <skill-directory>/scripts/validate_run_state.py <run-directory>
```

For `full-manuscript`, completion requires:

1. every material claim is linked to current evidence and within its claim ceiling;
2. the first two pages establish importance, question, evidence, and contribution without project-development language;
3. main-text exhibits carry the paper’s central argument;
4. each material caveat has one primary home;
5. the closest paper is represented fairly and differentiated economically;
6. fresh review finds no unresolved major prose or architecture problem;
7. numbers, references, citations, and rendered pages pass inspection; and
8. the final-hash cold-reader pass and the subsequent final whole-paper read form two consecutive acceptance reads and produce only copy-level comments.

For `section-revision`, completion instead requires:

1. every affected claim is linked to current evidence and within its claim ceiling;
2. the section opening states its economic job without development or weakness-first language;
3. claim-critical evidence and context are visible within the affected scope;
4. each affected caveat has one primary home;
5. closest-paper framing passes the fairness test when that comparison is in scope;
6. a hash-current cold read finds no unresolved major prose problem;
7. numbers, citations, exhibits, and terminology in the section pass inspection; and
8. the section and its surrounding transitions have been reread after the final edit.

If any condition is unverified, state that explicitly. Do not report the manuscript as finished.

## Output

Return:

- revised manuscript or prose;
- run artifact directory for manuscript-level work;
- concise issue summary;
- gate-status table;
- unresolved research or evidence questions kept outside the manuscript; and
- exact validation commands and results.
