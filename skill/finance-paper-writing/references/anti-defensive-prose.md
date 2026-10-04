# Anti-Defensive Prose

Candor and persuasion are compatible. Defensive prose becomes a problem when rebuttal arrives before the reader understands the claim, when negative statements substitute for a precise description of scope, or when repeated qualifications make the reader reconstruct the result from what the paper denies.

The objective is not stronger-sounding prose. It is **calibrated assertiveness**: state the strongest claim supported by the design, define its scope positively when possible, and place each material limitation where it changes inference.

## Core Rule

Advance the supported claim directly. Write as an author explaining an economic argument to a finance reader, not as an author negotiating with an imagined referee.

Never remove a limitation merely to make the paper sound more persuasive. If deleting a qualification would change the validity, interpretation, scope, research design, or proper use of a result, the qualification is material and must remain.

## Functional Diagnosis Before Rewriting

Before editing a defensive-looking sentence, classify its function. Do not treat every hedge or negative construction as equivalent.

| Function | Typical disposition |
|---|---|
| Unnecessary disclaimer | Delete |
| Redundant clarification | Delete or consolidate with its primary home |
| Necessary scope condition | Prefer positive scope when the same boundary can be stated precisely |
| Real methodological limitation | Retain once where it changes inference |
| Evidence-based qualification | Attach directly to the affected claim or interpretation |
| Useful conceptual contrast | Retain only when the contrast itself advances the economic argument |

Record material limitations in the caveat registry with both their function and disposition. In section-revision mode, scope the registry to caveats affected by that section rather than inventorying the whole paper. A limitation should not disappear merely because its original wording was defensive.

## Positive Scope

When possible, replace a negative boundary with the actual object the paper estimates, observes, predicts, compares, or identifies.

Weak:

> We do not claim that the disclosure measure identifies an exogenous treatment effect.

Better:

> The design estimates the predictive relation between disclosure content and subsequent firm-specific risk conditional on pre-disclosure controls.

Weak:

> The sample should not be interpreted as representative of all lenders.

Better:

> The sample covers publicly reporting U.S. lenders observed from 2001 through 2025.

Positive scope is not permission to overclaim. Use it only when the rewritten sentence preserves the same inferential boundary. If the omitted negative statement contains information that the positive description does not convey, keep a concise qualification at the point where it matters.

## Calibrated Uncertainty

Do not stack epistemic modifiers to manufacture caution.

Weak:

> The results may potentially suggest that the shock could perhaps affect refinancing activity.

Better when the design is predictive:

> The shock predicts lower refinancing activity over the next quarter.

Better when uncertainty is substantive:

> The estimate is imprecise in the post-2020 subsample, so the data do not distinguish a smaller effect from no effect in that period.

When uncertainty is real, identify its source: statistical precision, identification, measurement, external validity, theory, timing, or another concrete design feature. One specific boundary is more informative than several generic hedges.

Do not mechanically delete `may`, `could`, `suggests`, `appears`, or similar terms. Keep them when the evidence warrants them.

## Common Defensive Shapes

### Negative-first opening

Weak:

> Annual regressions cannot determine whether the disclosure causes the outcome.

Better:

> The measure predicts the subsequent distribution of firm-specific returns after conditioning on risk observed before the disclosure.

Add the causal boundary later if it is material to interpreting that evidence.

### Disclaimer chain

Weak:

> This result is not causal, does not identify a disclosure shock, does not isolate managerial intent, and should not be interpreted as an exogenous treatment effect.

Better:

> The estimates show that the disclosure contains information about subsequent firm-specific risk.

Use the design section or the affected interpretation to state why the evidence is predictive rather than causal.

### Comparator air defense

Weak:

> The two measures need not nest empirically because they use different sources, filters, denominators, and alignment rules.

Better:

> The neighboring measure captures reported shortages of available labor. This paper asks whether a broader set of disturbances to an organizational input carries incremental information about firm outcomes.

Methodological differences can be discussed after the economic distinction and evidence.

### Reviewer-directed prose

Weak:

> The appropriate test is therefore the asymmetric overlap rather than kappa.

Better:

> I test whether the broader measure retains explanatory content after removing observations identified by the narrower construct.

### Self-minimizing contribution language

Weak:

> This paper merely provides a preliminary attempt to examine the relation.

Better:

> This paper examines whether the relation predicts financing outcomes and identifies the settings in which it is strongest.

Do not replace modesty with unsupported novelty or importance claims. State the research job and evidence directly.

## Unfavorable, Null, and Mixed Evidence

A weaker specification, null, heterogeneous effect, failed robustness test, or adverse comparison is an empirical result before it is a "limitation."

For each unfavorable result:

1. determine whether it changes the central conclusion or its interpretation;
2. state the condition, estimate, metric, or comparison directly;
3. narrow or withdraw any claim that the result no longer supports;
4. distinguish a local boundary from a general defect; and
5. do not invent a mechanism for the unfavorable result when its cause is unknown.

Prefer:

> The relation is concentrated among firms with short debt maturity and is economically small in the long-maturity subsample.

over:

> One limitation is that the result does not hold everywhere.

If the result overturns the headline interpretation, say so. Anti-defensive editing must never hide adverse evidence.

## Reviewer-to-Manuscript Firewall

A referee simulation is a diagnostic tool, not a source of automatic manuscript caveats. Classify each reviewer comment as:

- **demonstrated defect**: a problem visible in the manuscript or evidence;
- **verification question**: a concern that requires checking before it is accepted as a problem; or
- **optional extension**: an additional analysis, discussion, or robustness request that is not necessary to support the current claim.

Only demonstrated defects, and verification questions that are verified as real problems, create a presumption of manuscript change. Optional extensions should not become limitations or defensive sentences merely because a reviewer could imagine them.

When a reviewer comment is accepted, repair the underlying claim, evidence, design explanation, or scope. Do not simply append a protective sentence.

## Caveat Registry

For each material limitation, record:

- limitation;
- claim affected;
- function;
- disposition;
- primary manuscript location;
- whether an earlier cross-reference is necessary; and
- final calibrated wording.

Default to one primary home and no repetition. Repeat only when the reader would otherwise materially misunderstand a later result.

Allowed dispositions should ordinarily be one of:

- `retain-here`;
- `relocate`;
- `positive-scope`;
- `merge-duplicate`; or
- `delete-noninformative`.

Use `delete-noninformative` only for an `unnecessary-disclaimer` or `redundant-clarification`. A necessary scope condition, methodological limitation, evidence-based qualification, or useful conceptual contrast may be rewritten, relocated, or merged, but not deleted as noninformative when it changes the reader's inference.

## Search Heuristics

Inspect concentrations of:

- cannot, unable, need not, not designed to;
- should not be interpreted;
- we do not claim, we do not attempt;
- this does not mean, this is not to say;
- the goal is not, rather than arguing;
- association is not causation;
- appropriate test;
- reviewers may worry;
- merely, modest attempt, preliminary attempt;
- to be clear, it is worth noting;
- nevertheless, despite, although, while at the start of sections;
- strings of `not X, not Y, and not Z`; and
- stacked epistemic modifiers such as `may potentially`, `might possibly`, or multiple uncertainty markers in one clause.

These terms are not forbidden. Flag density, placement, and function.

## High-Impact Positions

Apply stricter scrutiny to defensive language in:

- the abstract;
- the first two introduction pages;
- contribution paragraphs;
- section-opening sentences;
- the opening of the main empirical results; and
- the conclusion.

A necessary limitation can appear in a high-impact position when omitting it would materially misstate the claim. Otherwise state the supported result first and move the limitation to its primary home.

## Repair Rule

Do not simply delete qualifications or replace flagged words. Reconstruct the unit:

1. diagnose the defensive unit's function;
2. choose a disposition;
3. state the supported claim or positive scope;
4. present the evidence;
5. give the economic interpretation; and
6. include one limitation at the point where it changes inference.

If the qualification overwhelms the supported claim, reconsider whether the result belongs in the headline argument. If removing the qualification makes the claim false or materially broader, keep the qualification and narrow the claim instead.
