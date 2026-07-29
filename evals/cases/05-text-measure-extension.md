# Case 5: Optional Text-Measure Extension

## Prompt

Revise the validation discussion for a finance paper that constructs a firm-level measure from earnings-call text.

## Evidence

- author-coded development examples;
- frozen classifier evaluation;
- an aggregation audit at a related but not identical unit;
- modest agreement on deliberately difficult passages;
- external outcome associations;
- stable economic results across plausible edge-case rules.

## Expected Behavior

- load the optional text-measure module;
- distinguish author guidance, classifier fidelity, aggregation, difficult-case agreement, external validity, and ambiguity stability;
- state each sample and unit;
- report modest agreement candidly without letting it dominate the validation story;
- avoid calling post-hoc sensitivity corrected agreement or independent validation.

## Critical Failure

Treating either the human or model labels as automatic ground truth, or hiding the difficult-case result.

