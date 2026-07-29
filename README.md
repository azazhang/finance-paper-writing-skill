# Finance Paper Writing Skill

A prose-first, multi-pass workflow for drafting and revising empirical finance manuscripts with AI agents.

This skill addresses a failure that generic academic-writing tools often miss. An agent can produce grammatical, technically detailed prose that still reads unlike a finance paper: the draft leads with caveats, describes the research workspace instead of the research design, gives development diagnostics more attention than economic evidence, or anticipates referee objections before explaining the contribution.

The workflow treats those problems as failures of editorial judgment rather than word choice.

## What It Does

The skill enforces:

- an economics-first paper charter;
- a claim-to-evidence boundary before drafting;
- result-led finance prose;
- separation of manuscript, active development, and replication records;
- main-text evidence ordering from the reader’s perspective;
- disciplined treatment of caveats and noncausal evidence;
- fair closest-paper positioning;
- fresh read-only review after substantive edits;
- deterministic checks for recurring prose problems; and
- completion only after recorded whole-paper gates pass.

Its primary capability is manuscript prose. It does not replace empirical research design, literature discovery, generic proofreading, or LaTeX tooling.

## Activation Reliability

Installing a skill does not guarantee that an agent will select or follow it. This repository therefore uses four controls:

1. a broad trigger description covering common finance-manuscript requests and symptoms;
2. visible activation and persistent run artifacts;
3. machine-checked pass separation, review freshness, linter dispositions, and cold-reader scores; and
4. a short project routing rule for projects where skill selection has already failed.

For such projects, treat `docs/project-routing-rule.md` as part of installation rather than an optional refinement. Generic academic-paper, proofreading, and humanization skills may assist, but cannot substitute for these gates.

## Why Multiple Passes

One prompt should not ask an AI agent to be complete, cautious, technically precise, persuasive, and fluent at the same time. That combination commonly creates defensive and development-oriented prose.

This skill uses **one pass, one job**:

1. evidence boundary;
2. economic story;
3. section and exhibit architecture;
4. development-to-paper translation;
5. anti-defensive editing;
6. cold-reader context;
7. finance register;
8. independent finance-reader review;
9. forensic and rendered-paper checks.

The same agent may edit across passes, but it may not be the only final evaluator.

## Repository Structure

- `skill/finance-paper-writing/`: canonical Agent Skills package.
- `skill/finance-paper-writing/references/`: finance-writing rules and optional modules.
- `skill/finance-paper-writing/templates/`: paper charter, ledgers, and run state.
- `skill/finance-paper-writing/scripts/`: prose linter and run-state validator.
- `evals/`: generalized regression cases and scoring rubric.
- `tests/`: deterministic tests for the enforcement scripts.
- `scripts/`: repository installation and verification tools.
- `docs/project-routing-rule.md`: optional project-level activation rule when automatic routing is unreliable.

The canonical skill is provider-neutral. The installer places the same package in the selected Agent Skills directory for Codex, Claude Code, or Cursor, avoiding divergent copies.

If a finance project has repeatedly bypassed installed writing skills, add the short rule in `docs/project-routing-rule.md` to that project’s agent instructions. The installer does not modify global instruction files automatically because instruction crowding can make routing less reliable.

## Install

Preview installation:

```bash
python3 scripts/install_local.py --dry-run
```

Install for Codex:

```bash
python3 scripts/install_local.py --providers codex
```

Install for several Agent Skills-compatible tools:

```bash
python3 scripts/install_local.py --providers codex,claude,cursor
```

Use `--mode copy` instead of the default symlink when preferred.

## Verify

```bash
python3 scripts/verify_repo.py
python3 -m unittest discover -s tests -v
python3 scripts/verify_local_install.py --providers codex
```

The skill-definition validator can also be run directly:

```bash
uv run python /path/to/validate_skill.py skill/finance-paper-writing --strict
```

## Typical Requests

- “Rewrite this introduction so it reads like an empirical finance paper.”
- “Audit the manuscript for defensive prose and internal development language.”
- “Revise the paper from first principles and make the main evidence visible.”
- “Position this paper against its closest finance paper without an air-defense tone.”
- “Check whether the abstract, introduction, tables, and conclusion tell the same story.”

## Optional Text-Measure Module

The universal workflow does not assume the paper constructs a text measure. When that design is present, an optional module adds guidance for presenting human coding, classifier fidelity, aggregation, disagreement, economic validation, and sensitivity to ambiguous classifications.

## Sharing

The repository is structured for publication as a standalone GitHub project. It uses the MIT License, matching the companion finance-literature-review skill repository.
