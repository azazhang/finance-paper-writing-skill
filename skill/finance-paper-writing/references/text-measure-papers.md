# Optional Module: Text-Based Measures

Load this module only when a finance paper constructs or validates a measure from text, human coding, a classifier, or LLM labels.

Do not import its terminology or checklist into ordinary empirical finance papers.

Record the module when initializing a run:

```bash
python3 <skill-directory>/scripts/init_run.py <main-file> \
  --mode <mode> --module text-measure
```

Enable the same module when running the prose linter:

```bash
python3 <skill-directory>/scripts/finance_prose_lint.py <source> \
  --manuscript <main-file> --module text-measure
```

## Measurement Evidence Map

Distinguish:

| Evidence | Question answered |
|---|---|
| Construct definition and coding examples | What economic boundary does the measure intend to capture? |
| Author or human guidance | How did economic judgment enter development? |
| Frozen-sample classifier fidelity | How closely does the operational classifier reproduce its reference labels? |
| Aggregation audit | Does sentence or document classification yield the intended empirical-unit measure? |
| Difficult-case agreement | Where does interpretation remain ambiguous under a stated protocol? |
| Convergent validity | Does the measure relate to nearby constructs as expected? |
| Discriminant validity | Is it distinct from generic tone or a neighboring construct? |
| Known-groups validity | Is the measure stronger where economics predicts greater exposure? |
| External or predictive validity | Does it relate to outcomes outside the labeling exercise? |
| Ambiguity stability | Do economic conclusions survive plausible treatments of edge cases? |
| Source and threshold robustness | Does implementation choice drive the result? |

## Hard Boundaries

- Teacher–student or LLM–classifier agreement is fidelity to the reference labeler, not independent validation.
- A deliberately difficult sample is not automatically a population reliability estimate.
- Human labels are a stated reference protocol, not automatic ground truth.
- A post-hoc reinterpretation is a diagnostic, not a new independent IRR estimate.
- Report the sampling frame, unit, prevalence, and reference source for every agreement statistic.
- Match aggregation evidence to the empirical unit whenever feasible.
- Do not let one familiar classification statistic define the validation story.
- Do not hide weak agreement; state its scope and show whether economic conclusions depend on plausible edge-case classifications.

## Main-Text Presentation

Give main-text prominence according to relevance to the paper’s economic claim:

1. construct and representative examples;
2. evidence that the aggregated measure behaves as intended;
3. economic, external, convergent, and discriminant validity;
4. classifier and agreement diagnostics with exact scope;
5. ambiguity and implementation sensitivity.

This is not a fixed table order. A salient weakness may require visible treatment. The objective is a balanced validation argument rather than either concealment or caveat dominance.

## Language

Prefer:

- author-coded examples;
- reference classifications;
- classifier fidelity;
- aggregation audit;
- difficult excerpts;
- alternative coding rules;
- economic conclusions are stable across plausible definitions.

Avoid:

- gold standard without justification;
- autonomous validation;
- corrected kappa for a post-hoc diagnostic;
- human principal investigator;
- teacher and student in the abstract or introduction;
- deployment, model generation, or internal version labels in reader-facing prose.
