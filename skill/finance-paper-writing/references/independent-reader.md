# Integrated Manuscript Reading and Independent Scholarly Reading

## Governing sequence

The writer owns the finished argument. For a substantive whole-paper writing or revision assignment, **write → read the assembled manuscript as a finance scholar → repair it → consider one fresh independent reading → resolve material feedback → deliver**. The integrated reading is a required part of the writer's work; an independent reader is a bounded second perspective, never a replacement for the writer's own reading. Apply the scale of the assigned task. No charter, recorded gate, score, or extra approval artifact is required.

This guidance governs the ordinary manuscript-writing workflow. A user-requested stand-alone review may be conducted as a review directly. An explicitly selected legacy formal-run package has its own record schema and validation rules; those do not apply to normal prose writing.

## Writer's integrated reading: required for a substantial whole-paper revision

Once the substantive writing is assembled, the **writing agent itself** must read the current manuscript, not an outline, a change log, selected paragraphs, or its memory of what it intended. Prefer the **rendered PDF**, main text in reading order from title and abstract through conclusion, with the principal tables/figures, captions, and notes interpreted where referenced. If no rendered PDF can be produced, read the assembled manuscript text and exhibits in actual order; treat unavailable rendering as a specific limitation if material to the requested output.

Perform this as a real reading with responsibility for directly repairing the manuscript:

1. **Economic spine:** The abstract and introduction establish the same question that the design and main results answer. The conclusion conveys the same supported answer and incremental contribution. The argument progresses from economically consequential uncertainty to decisive evidence and interpretation.
2. **Cross-section identities:** Definitions of constructs, sample, population, units, denominators, groups, horizons, dates, treatment/exposure, empirical design, and claim strength remain stable across abstract, introduction, design, exhibits, results, and conclusion. Reconcile every contradiction using the established evidence; do not paper over disagreement by adding hedges.
3. **Paragraph-to-paragraph continuity:** Each paragraph builds on the previous one or introduces a clear next economic step. Remove patchwork symptoms: duplicate contributions, repeated background, conflicting explanations, stranded transitions, abrupt topic changes, undefined acronyms, stale passages from earlier versions, or sentences whose referents have changed.
4. **Exhibit-to-prose fit:** The named exhibit actually shows the stated quantity and comparison. Check main estimates, directional conclusions, scale, reference group, uncertainty, and interpretation using the current evidence. Position the strongest exhibit where the argument needs it.
5. **Publication register:** The whole paper reads as one coherent scholarly finance article. Eliminate prose that sounds like research-development notes, artificial model rhetoric, disconnected technical summaries, or defensive referee responses. Preserve material limitations and contradictory evidence that change inference.

**Repair the actual text and references**, then reread the affected transitions and, when structural changes are broad, the revised assembled paper. Do not send the independent reader an obvious compilation of incompatible fragments. Do not claim this reading occurred unless the writer actually encountered the assembled manuscript. This is authorship, not a separate reviewer job or a mandatory self-review report.

For a **section rewrite**, read the full affected section, its adjacent transitions, and other headline passages only insofar as the change alters their claims. For a **single passage or small correction**, read the edited unit and immediately surrounding context. Do not manufacture a whole-paper review for a local edit.

## When to request a fresh independent scholarly reading

After the writer's integrated reading and substantive repairs, a **single bounded scholarly cold reading** is the normal choice for a substantial whole-paper reconstruction **when** a genuinely separate reader/context is available, permitted, and materially useful. It remains optional under user or project restrictions; lack of a separate reader is not a reason to delay or fail an otherwise completed writing assignment. For a limited section rewrite, use a reader only if a specific material communication uncertainty persists or the user asks. For simple changes, proceed without one.

An independent assessment is a tool for the **reader's actual comprehension**, not a simulated journal acceptance decision. A different model family may provide a useful perspective when authorized, but model difference is no guarantee of independence or accuracy. Do not launch other agents solely to satisfy a process requirement when tools or permissions do not support it.

Give the cold reader only the latest complete manuscript and its relevant exhibits, the scholarly finance publication-voice standard, and the narrow reading assignment. Avoid preparatory worklogs, author explanations, prior reviewer comments, and draft intentions that would let the reader reconstruct an argument absent from the paper itself. If the user explicitly requests a referee assessment, follow that separate scope.

## Cold reader's actual intellectual job

**First reconstruct the argument from the paper alone**, before critiquing it:

- What is the economically consequential question and why does it matter?
- What does the manuscript's research design or comparison actually identify or describe?
- What is the principal finding, with its meaningful magnitude and horizon?
- What mechanism or competing explanation does the evidence illuminate?
- What is the substantive increment over the closest literature?

If any answer is unclear, point to the **exact passage, exhibit, or transition** where the argument becomes difficult to recover. A reader should report what the text conveyed, without guessing what the writer intended.

Then return only the **few material, evidence-grounded scholarly-communication problems** affecting the central argument, coherence, evidence prominence, publication register, or calibrated interpretation. For each, give the location, what the text actually communicates, why that is misleading or confusing, and the kind of revision needed. There is no required minimum issue count. Do not manufacture objections, propose new robustness grids, perform a full scientific referee simulation, or treat optional extensions as manuscript defects.

Classify a consequential comment as:
- **Demonstrated writing defect:** visible inconsistency, unsupported interpretation, misleading structure, or missing context in the manuscript/exhibit.
- **Verification question:** a concrete factual or inferential concern needing a targeted check before editing.
- **Optional extension:** an interesting but nonessential new argument, analysis, or additional paper objective.

No scores, pass/fail thresholds, acceptance certificates, or publication-readiness claims.

## Writer's response and stopping rule

The writing agent evaluates reader comments independently against the paper and current evidence. **Implement demonstrated writing repairs directly**. Verify consequential factual questions before accepting them. Honor the established scope: optional extensions do not authorize additional estimation or defensive manuscript caveats. The reader's suggested wording is advisory; the writer is responsible for a better scholarly argument.

After repairing material issues, read the **affected prose and its transitions** and check any changed main claims or exhibits. Do not automatically send the manuscript for another reading. A further independent reading requires an explicit user request or a genuinely new, substantial reconstruction of the central economic argument that makes the earlier reading inapplicable; it is a distinct, justified action, not a score-seeking loop. Stop when the requested manuscript is coherent and the substantive revision is complete.

## Separation from other checks

- **Writer's integrated read**: mandatory authorship for substantial whole-paper writing; it repairs obvious inconsistencies and stitched-together prose.
- **Independent scholarly cold read**: optional, fresh comprehension of the finished argument after writer repair; bounded feedback.
- **Evidence consistency verification**: check affected quantitative statements and citations against their actual sources during writing.
- **Scientific referee review**: separate user-authorized research assessment of identification, contribution, measurement, mechanisms, and potential additional analyses.

The optional `init_run.py` and `validate_run_state.py` default to a concise writer-first formal record (schema v3) that requires no approval scores, reader cycles, or cold-reader acceptance. Independent reading has a record only if selected separately. Historic v1/v2 records and elaborate multi-pass templates remain accessible in the `templates/legacy/` archive. A passing validator result establishes record and hash consistency; it cannot establish research quality or prove that the agent truly read the manuscript.

*The bounded-reader and non-convergence design draws on Manish Jha, “AI for Finance Research” (https://mjha91.github.io/pdf/AIFinanceResearch.pdf), and on repeated observed manuscript-workflow failures.*