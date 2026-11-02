# Finance Paper Writing Skill

**A paper succeeds by making a clear, falsifiable economic argument and putting its sharpest quantitative evidence front and center.** This skill helps an AI agent draft and revise empirical finance papers around that standard.

It addresses an editorial failure that grammar tools miss: a technically correct manuscript can still hide its economic question, catalogue disconnected estimates, lead with qualifications, or sound like a development report. The remedy is an argument supported by interpretable evidence and natural finance prose.

## What It Does

- Organizes the abstract, introduction, results, exhibits, and conclusion around the same economic argument.
- Selects main-text and Appendix evidence for its inferential role, while preserving exploration in the research record.
- Uses direct claims calibrated to the design, with one primary home for material qualifications.
- Represents neighboring literature fairly and distinguishes contributions economically.
- Maintains finance register through later revisions, including headings and exhibit notes.
- Scales work to the requested revision instead of requiring process artifacts for every edit.

The principle **one pass, one job** helps separate argument, interpretation, authorial voice, and reader context when a broad revision needs that attention. It does not require eight logs, repeated whole-paper reads, a score threshold, or a new review campaign.

Installing a skill does not guarantee adherence. The revised manuscript is the deliverable. A linter pass, recorded workflow, page count, or successful compilation does not certify a scholarly contribution.

## Repository Structure

- `skill/finance-paper-writing/`: the single canonical skill package.
- `references/` inside the package: prose standards and topic-specific guidance.
- `examples/`: before-and-after illustrations.
- `scripts/finance_prose_lint.py`: optional diagnostic aid.
- Other bundled scripts and templates: retained support for an explicitly requested formal review record or historical runs. They are not prerequisites for ordinary revision.
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
