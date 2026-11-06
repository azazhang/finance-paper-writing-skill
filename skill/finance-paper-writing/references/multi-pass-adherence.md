# Proportionate Revision and Optional Workflow Tools

Apply the prose standard continuously. A skill name, a plan, or recorded compliance did not prevent earlier failures because the agent could complete the process while leaving the economic argument obscure. Judge the actual revision.

## Default revision

Use the current manuscript and established evidence. Make the requested substantive change, then read the affected prose and transitions. For a broad revision, focus attention on argument and evidence order before sentence-level work. Check numbers and references that changed, compile edited LaTeX, and inspect affected layout. After substantive whole-paper writing, the same writer reads the assembled manuscript from beginning to end and fixes inconsistencies and stitched-together prose before a cold reader is considered. Existing research notes can retain decisions; do not create another artifact set merely to show that attention was paid.

A useful separation is “one pass, one job”: economic architecture, evidence interpretation, authorial voice, reader context, and finance register are different editorial problems. Choose the work needed for the assignment. These are not mandatory logged stages, and a simple change does not require a whole-paper cycle.

## Writer-first integration and bounded independent reading

For a substantial full-manuscript revision, the writer must **read the assembled manuscript** (preferably its rendered PDF) and repair the argument across sections: conflicting definitions or estimates, mismatched conclusions, duplicated text, broken transitions, and patchwork paragraphs. This belongs to substantive manuscript completion; do not outsource it to another reader or replace it with a log, outline, or skim alone. For a local revision, inspect the affected text and transitions. Detailed instructions are in [independent-reader.md](independent-reader.md).

After the writer's integrated repair, a fresh reader may be used when requested or when one bounded reading would materially improve a substantial manuscript's communication, subject to user restrictions and availability. The reader first reconstructs the question, main evidence, economic answer, and contribution from the manuscript itself and reports only a few grounded communication issues. Classify any proposal as a demonstrated defect, verification question, or optional extension. The writer repairs demonstrated problems and verifies consequential questions without automatically launching more review rounds.

Do not turn imagined objections into caveat catalogues or pursue reviewer scores. One independent read is normally enough; rerun only if explicitly requested or a substantial reconstruction makes the prior read obsolete. The legacy formal package's scores and review requirements do not govern ordinary manuscript work.

## Optional formal full-manuscript run package

`init_run.py` is a script because it **creates files and records**: a run directory, copies of structured templates, a pass log, run metadata, and a baseline manuscript hash. Markdown guidance explains editorial practice; this executable helper initializes an optional formal record when the author explicitly requests one. It defaults to `full-manuscript`, with earlier `section-revision` and `prose-audit` modes preserved for existing uses. `validate_run_state.py` validates the selected formal record, including its required passes, reader records, and hashes. Its strict schema applies only to a deliberately initialized formal run. `manuscript_hash.py` also supports the standalone prose linter. The ordinary workflow is editing the manuscript directly; no formal run is implied by a full-paper writing request alone.

A formal package is inappropriate when it would violate project prohibitions, repeat completed work, or displace the requested revision. A validator checks its record format; it cannot establish the economic contribution, validity, identification, or quality of the prose. Neither a passing package nor a manuscript length certifies publication readiness.

The prose linter can be run independently without initializing a package. Treat matches as leads, preserve appropriate finance terms, and read the surrounding passage before changing it.

## Completion

Completion means the assigned revision has been implemented, its changed claims match the evidence, and the resulting prose and rendering have been checked at the scale of the task. For substantial full-paper work, the writer actually reads and repairs the assembled manuscript before considering independent reading. Report the substantive change and remaining decision-relevant issues. Do not report a workflow certificate in place of the paper.