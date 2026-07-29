# Repository Context

This repository packages a prose-first empirical-finance manuscript workflow for multiple AI agents.

## Canonical Source

`skill/finance-paper-writing/` is the canonical skill package.

Do not maintain separate provider copies of `SKILL.md`, references, templates, examples, or enforcement scripts. Provider adapters must point users or installers to the canonical package.

## Working Rules

- Treat finance-manuscript prose as the primary capability.
- Keep the universal workflow applicable to empirical finance generally.
- Keep text-measure and classifier guidance in the optional module.
- Preserve the distinction between manuscript evidence, active development, legacy material, and replication records.
- Require recorded gates and fresh read-only review for manuscript-level completion.
- Never weaken a material limitation merely to make prose more persuasive.
- Never add generic compliance sections without a venue or study-specific reason.
- Keep provider instructions aligned with the canonical skill.
- Add a regression case when fixing a recurring workflow failure.
- Run repository verification and unit tests after changes.

## Validation

```bash
python3 scripts/verify_repo.py
python3 -m unittest discover -s tests -v
```

Also run the external skill validator against `skill/finance-paper-writing/` when available.

