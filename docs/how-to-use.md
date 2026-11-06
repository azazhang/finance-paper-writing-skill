# How to Use

## Whole paper

> Use finance-paper-writing to revise this empirical finance paper. Make the economic argument and sharpest evidence clear, preserve claim calibration, and keep the abstract, introduction, results, and conclusion coherent.

The agent should read the current manuscript and relevant established evidence, construct and implement the requested economic argument and prose (including introduction and contribution), check affected quantitative claims against cited exhibits and literature statements against sources, and compile edited LaTeX. **Before delivery or an independent reader, the writer must read the assembled paper from title through conclusion**, preferably as a rendered PDF with exhibits encountered in context, and directly repair conflicting definitions, magnitudes, contradictory claims, incoherent transitions, duplicated paragraphs, and text left over from earlier drafts. Reread affected passages after repair. A new charter, run directory, scorecard, or reviewer campaign is not required.

## Section or passage

> Revise the introduction so a finance reader understands the tension, question, main finding, and contribution after the first two pages.

> Rewrite this abstract as connected prose. Keep the sharpest quantitative evidence and explain its economic meaning.

> Rewrite this paragraph in empirical-finance register while preserving the supported claim.

Read the affected section and its necessary transitions after editing. A local change requires proportionate local coherence checks; the assembled-paper reading belongs to substantial whole-paper tasks. Do not promote a paragraph revision into a full research restart.

## Review when requested

> Read this paper and identify the few structural problems that prevent its argument from being understood. Do not edit or start new empirical work.

Follow [independent-reader.md](../skill/finance-paper-writing/references/independent-reader.md). For a writing task, the authoring agent performs its integrated manuscript reading and repairs first. Then use one fresh reader when available, permitted, and useful, normally for a substantial whole-paper reconstruction. Give the reader the finished manuscript and relevant exhibits without development logs. The reader reconstructs question, evidence, answer, and contribution before identifying a few grounded communication defects. Distinguish demonstrated defects, verification questions, and optional extensions. The writer repairs justified problems and stops; do not run serial AI referees or optimize scores. For a direct, user-requested review, review the manuscript as requested without inventing a preparatory writing stage.

## Text-based measures

Use the optional text-measure reference when presenting a text construct. Describe the established measure and its actual validity evidence. A writing task does not authorize another source-reading, classifier, or coding cycle.

## Scholarly publication voice and economic contribution

For every substantive finance-manuscript writing task, apply `references/voice-calibration.md` alongside the finance prose rubric. The primary target is the writing convention of scholarly financial economics: economic question, mechanism, informed comparison, inferentially calibrated claim, interpreted magnitude, and contribution to knowledge. The reference annotates verified JF/JFE/RFS examples; its distilled guidance ordinarily suffices without opening exemplar articles again. Draft the requested section yourself using the study's established evidence.

When effective author- or coauthor-approved passages already exist, preserve their natural terminology and rhythm as secondary preferences consistent with scholarly finance style. No mandatory personal voice profile, source-collection campaign, or approval cycle is needed.

For a substantive introduction or results revision, connect the economically important unresolved question, plausible mechanisms, decisive quantitative comparison, and incremental insight. Reconcile the affected magnitudes, units, uncertainty, and exhibit references directly with established results.

## GPT/Codex anti-defensive guidance

For every finance-manuscript prose revision by Codex or any GPT-family model, read and apply `references/anti-defensive-prose.md` even when editing a single sentence. When underlying model identity is unknown, apply it. Confirmed non-GPT/non-Codex agents may use it selectively. Apply the standard during writing and check the affected passage; no separate audit report is needed.

## Optional formal full-paper records

For an **explicitly requested** formal record, run `skill/finance-paper-writing/scripts/init_run.py MANUSCRIPT --lead-editor WRITER`. The default schema v3 records current manuscript hashes and gives the writer `writer-integration.md` to complete after actually reading and repairing the assembled manuscript. Set the final and writer-read hashes in `run.json` and validate with `validate_run_state.py RUN_DIRECTORY`. Add `--with-independent-reader` only when a fresh reader is separately selected; reviewer notes may refer to the previous manuscript version before the writer’s final repairs. **No eight-pass log, reviewer score, acceptance threshold, or mandatory cold reader** applies. Historical schema-v1/v2 records remain supported in `templates/legacy/`; `--legacy-format` initializes that deprecated structure solely for compatibility. Formal records are never automatically required for full-paper writing, and successful validation establishes provenance and record completeness only.

## Report back

Explain the substantive argument, interpretation, and passages improved in self-contained prose. Link the revised manuscript or compiled PDF when relevant. Mention a remaining consequential research decision directly. Do not substitute worklogs or process status for the paper.