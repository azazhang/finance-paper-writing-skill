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



## Why deterministic helper tests are insufficient

The Python unit tests prove narrowly specified scanner and validator behavior. They do not score economic arguments, diagnose stitched-together manuscripts, evaluate journal-style prose, or show that an AI agent followed the skill. An explicitly poor, generic finance paragraph is included as a **zero-pattern-match negative control**. Absence of flags is expected and must never be called a clean manuscript.

The behavioral cases require fresh writing agents actually to produce revised prose. In particular, cases 17 and 18 test whether the agent completes a contribution with incomplete neighboring-study detail and whether it rewrites weak academic prose even after the regex scanner finds zero matches. Merely adding cases does not establish that agents will succeed; record real agent outputs and analyze their scholarly content when a behavioral evaluation is run.
