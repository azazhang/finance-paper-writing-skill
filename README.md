# Finance Paper Writing Skill

**A paper succeeds by making a clear, falsifiable economic argument and putting its sharpest quantitative evidence front and center.** This skill helps an AI agent draft and revise empirical finance papers around that standard.

It addresses an editorial failure that grammar tools miss: a technically correct manuscript can still hide its economic question, catalogue disconnected estimates, lead with qualifications, or sound like a development report. The remedy is an argument supported by interpretable evidence and natural finance prose.

**GPT-family models and Codex must read and apply `skill/finance-paper-writing/references/anti-defensive-prose.md` for every manuscript-prose edit, including single-sentence changes.** When the model family is uncertain, apply it; models known to be neither GPT nor Codex may consult it as a reference. This is a writing standard throughout the edit, with no separate compliance ritual.

## What It Does

- Develops the introduction, contribution, interpretation, and conclusion around a financially consequential economic question and an evidence-supported answer.
- Organizes the abstract, introduction, results, exhibits, and conclusion around the same economic argument.
- Selects main-text and Appendix evidence for its inferential role, while preserving exploration in the research record.
- Uses direct claims calibrated to the design, with one primary home for material qualifications.
- Represents neighboring literature fairly and distinguishes contributions economically.
- Calibrates substantive writing to the scholarly publication register of financial economics, with individual author preferences preserved as a secondary consideration.
- Requires the writing agent to read and repair the assembled manuscript after substantial whole-paper work, before an optional fresh independent reading.
- Scales work to the requested revision instead of requiring process artifacts for every edit.

The principle **one pass, one job** helps separate argument, interpretation, and reader context. For substantial full-paper work, the writer must read the actual assembled manuscript in reading order and repair contradictions, patchwork paragraphs, and broken transitions. One independent scholarly cold reading may follow when useful and permitted; its purpose is fresh comprehension and its feedback prompts targeted repairs. Neither activity requires a score threshold, acceptance gate, mandatory reviewer campaign, or repeated cycles.

Installing a skill does not guarantee adherence. The revised manuscript is the deliverable. A linter pass, recorded workflow, page count, or successful compilation does not certify a scholarly contribution.

## Repository Structure

- `skill/finance-paper-writing/`: the single canonical skill package.
- `references/` inside the package: core scholarly-finance voice calibration, writer-first manuscript integration and independent-reading guidance, prose standards, evidence checks, and conditional topic-specific guidance.
- `examples/`: original, synthetic finance-manuscript passages illustrating argument construction and quantitative interpretation. The separate scholarly voice reference draws lessons from verified published examples; author-specific style is secondary.
- `skill/finance-paper-writing/scripts/finance_prose_lint.py`: optional diagnostic aid; `manuscript_hash.py` supports LaTeX input discovery and hashing.
- `init_run.py`, `validate_run_state.py`, and templates: executable tooling for an **optional formal full-manuscript pass** when explicitly selected. The initializer automates files, pass logs, and hashes; its legacy section-revision and audit modes remain available for compatibility. Ordinary manuscript revisions are direct writing tasks.
- `evals/` and `tests/`: behavioral cases and deterministic helper tests.

The same provider-neutral package is installed for Codex, Claude Code, or Cursor. No separate provider copies are maintained.

## Install

```bash
python3 scripts/install_local.py --dry-run
python3 scripts/install_local.py --providers codex
```

For several supported roots:

```bash
python3 scripts/install_local.py --providers agents,codex,claude,cursor
```

Use `--mode copy` when preferred. Managed copies with local edits are protected from replacement unless explicitly discarded. The optional short rule in `docs/project-routing-rule.md` can improve routing in a finance project; installation does not modify global instructions.

## Verify

```bash
python3 scripts/verify_repo.py
python3 -m unittest discover -s tests -v
python3 scripts/verify_local_install.py --providers agents,codex,claude,cursor
```

Skill-definition validation checks the package, not whether its advice produces a good paper. Use the task-relevant guidance in `docs/how-to-use.md`; do not treat the helper tests as a manuscript acceptance process.