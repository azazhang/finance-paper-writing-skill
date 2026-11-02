# Evaluation Protocol

These cases test failures that survived ordinary academic-writing and proofreading guidance.

## Baseline and Treatment

For each case:

1. give the prompt and draft to a fresh agent without this skill;
2. save the response;
3. repeat with `finance-paper-writing` explicitly active;
4. give both outputs, in random order, to a separate evaluator;
5. score using `rubric.md`; and
6. record new recurring failures before changing the skill.

Do not use the agent that designed the skill as the only evaluator.

## Passing Standard

- no critical failure;
- at least 14 of 16 rubric points;
- no measure-specific terminology in the standard corporate-finance case;
- no development-language or local-path leakage; and
- the evaluator can recover the intended economic question, result, contribution, and claim boundary.

These are optional development evaluations for changes to the skill, not mandatory stages of each manuscript revision. Deterministic tests cover helper behavior, including the retained formal-record schema. They do not establish editorial judgment or publication quality.

