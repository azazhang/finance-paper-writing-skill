# Proportionate Revision and Optional Workflow Tools

Apply the prose standard continuously. A skill name, a plan, or recorded compliance did not prevent earlier failures because the agent could complete the process while leaving the economic argument obscure. Judge the actual revision.

## Default revision

Use the current manuscript and established evidence. Make the requested substantive change, then read the affected prose and transitions. For a broad revision, focus attention on argument and evidence order before sentence-level work. Check numbers and references that changed, compile edited LaTeX, and inspect affected layout. Existing research notes can retain decisions; do not create another artifact set merely to show that attention was paid.

A useful separation is “one pass, one job”: economic architecture, evidence interpretation, authorial voice, reader context, and finance register are different editorial problems. Choose the work needed for the assignment. These are not mandatory logged stages, and a simple change does not require a whole-paper cycle.

## Bounded independent reading

A reader can identify whether the paper's question, result, and contribution are recoverable. Use one when requested or when it answers a concrete structural question efficiently and within the user's restrictions. Classify comments as a demonstrated defect, an unresolved verification question, or an optional extension before acting. Fix demonstrated problems; verify a consequential concern before treating it as true; keep optional work outside the manuscript unless the author expands the assignment.

Do not turn a reader's imagined objections into a caveat catalogue. Do not repeat review until the paper earns a score. Review is useful for a specific question, not a substitute for the author's judgment or an automatic condition of every revision.

## Optional formal full-manuscript run package

`init_run.py` is a script because it **creates files and records**: a run directory, copies of structured templates, a pass log, run metadata, and a baseline manuscript hash. Markdown guidance explains editorial practice; this executable helper initializes an optional formal record when the author explicitly requests one. It defaults to `full-manuscript`, with earlier `section-revision` and `prose-audit` modes preserved for existing uses. `validate_run_state.py` validates the selected formal record, including its required passes, reader records, and hashes. Its strict schema applies only to a deliberately initialized formal run. `manuscript_hash.py` also supports the standalone prose linter. The ordinary workflow is editing the manuscript directly; no formal run is implied by a full-paper writing request alone.

A formal package is inappropriate when it would violate project prohibitions, repeat completed work, or displace the requested revision. A validator checks its record format; it cannot establish the economic contribution, validity, identification, or quality of the prose. Neither a passing package nor a manuscript length certifies publication readiness.

The prose linter can be run independently without initializing a package. Treat matches as leads, preserve appropriate finance terms, and read the surrounding passage before changing it.

## Completion

Completion means the assigned revision has been implemented, its changed claims match the evidence, and the resulting prose and rendering have been checked at the scale of the task. Report the substantive change and remaining decision-relevant issues. Do not report a workflow certificate in place of the paper.