# Repository Context

This repository packages a prose-first empirical-finance manuscript workflow for multiple AI agents.

## Canonical Source

`skill/finance-paper-writing/` is the canonical skill package.

Do not maintain separate provider copies of `SKILL.md`, references, templates, examples, or enforcement scripts. Provider adapters must point users or installers to the canonical package.

## Working Rules

- Treat finance-manuscript prose as the primary capability, calibrated to the publication conventions of financial economics.
- Keep the universal workflow applicable to empirical finance generally.
- Keep text-measure and classifier guidance in the optional module. Treat voice-calibration.md as a core scholarly-finance publication standard for substantive prose; use personal authorial style only as a secondary preference and avoid a new voice-profile stage.
- Preserve the distinction between manuscript evidence, active development, legacy material, and replication records.
- Scale revision to the assigned task. Keep formal run artifacts optional and use bounded independent reading only when it serves a concrete need within user restrictions.
- Make the economic argument and strongest quantitative evidence the primary standard. Agents assigned introductions, contribution paragraphs, and results interpretations must draft the substantive economic answer from the author's evidence rather than offering only reviewer comments or outlines. Do not certify prose or publication quality from helper-script success.
- Never weaken a material limitation merely to make prose more persuasive.
- Never add generic compliance sections without a venue or study-specific reason.
- For Codex and GPT-family models, keep the anti-defensive-prose reference active on every finance-manuscript prose edit, including small edits; use it when model identity is uncertain. Other known model families can consult it selectively.
- Keep provider instructions aligned with the canonical skill.
- Add a regression case when fixing a recurring workflow failure.
- Run repository verification and unit tests after changes.

## Validation

```bash
python3 scripts/verify_repo.py
python3 -m unittest discover -s tests -v
```

Also run the external skill validator against `skill/finance-paper-writing/` when available.