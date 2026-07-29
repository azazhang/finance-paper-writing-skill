# How to Use

## Full Manuscript

Ask:

> Use finance-paper-writing to revise this empirical finance manuscript from first principles. Treat prose as the primary problem, preserve the evidence boundary, and use a fresh finance reader before declaring completion.

The agent should:

1. announce skill use;
2. initialize `.finance-writing/runs/...`;
3. complete the charter and evidence ledger;
4. audit macro prose before editing;
5. run distinct rewrite passes;
6. obtain a hash-current cold read;
7. run deterministic and forensic checks; and
8. return a gate-status table.

## Section Revision

Ask:

> Revise the introduction with finance-paper-writing. Diagnose argument order and defensive prose before rewriting, then run a cold-reader check on the revised section.

The section still needs a charter excerpt and evidence mapping. It does not require a complete whole-paper convergence exercise.

## Read-Only Audit

Ask:

> Audit this manuscript’s prose using finance-paper-writing. Do not edit. Focus on development-language leakage, weakness-first exposition, evidence prominence, closest-paper framing, reader context, and repetitive caveats.

The output should be a severity-ranked issue ledger, not a generic referee report.

## Isolated Passage

Ask:

> Rewrite this paragraph in empirical-finance register. Preserve the supported claim and explain why the original reads defensively.

The lightweight mode does not create a run directory.

## Text-Based Measure

Ask:

> This paper constructs a measure from text. Use the optional text-measure module, but keep its validation vocabulary out of the general economic story unless needed.

## What Good Completion Looks Like

The handoff should identify:

- manuscript files changed;
- substantive prose problems corrected;
- main evidence moved or reframed;
- independent reviewer identity and manuscript hash;
- unresolved research issues kept outside the paper;
- deterministic validation commands and results; and
- any gate that remains unverified.

