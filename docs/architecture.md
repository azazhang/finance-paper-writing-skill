# Architecture

## Design Goal

The capability is empirical-finance manuscript prose: an economically meaningful argument, decisive interpretable evidence, and natural authorial exposition. The skill guides editorial choices rather than attempting to certify them through a mandatory control system.

## Canonical Source

`skill/finance-paper-writing/` is the single substantive package. Provider installations point to or copy it, avoiding divergent instructions.

## Guidance and Optional Tools

The entrypoint makes the agent responsible for actually drafting the economic argument, including introduction and contribution when assigned, using the author's established evidence and direction. It contains the central standard, proportionate revision guidance, and routes to relevant references. The anti-defensive and finance-register references govern the actual prose. For GPT-family models and Codex, anti-defensive guidance is mandatory on **every** revision, including small edits; when model identity is unknown, apply it. Agents confirmed to be neither may treat it as a conditional reference. Scholarly [voice calibration](../skill/finance-paper-writing/references/voice-calibration.md) is a core standard for substantive manuscript writing, using grounded examples from published JF/JFE/RFS work to teach disciplinary conventions. Existing author-approved prose remains useful for secondary personal preferences. There is no separate style-profiling or benchmark-reading requirement. The text-measure module is conditional; ordinary finance papers do not inherit classifier terminology.

The linter supplies optional diagnostic leads and uses the LaTeX manuscript-hash utility. When explicitly requested, the initializer creates a **schema-v3 writer-first formal record**, with manuscript hashes, the writer’s integrated-reading notes, and an independent-reader record only with `--with-independent-reader`. The validator checks hash freshness and selected records, without eight mandatory passes, score thresholds, or cold-reader approval. Historical schema-v1/v2 records remain readable; the old templates live in `templates/legacy/` and can be initialized only with `--legacy-format` for compatibility. These optional tools never replace ordinary writing; validation certifies record consistency, not argument quality.

Earlier mandatory artifact and repeated-review requirements encouraged process to displace the requested revision. Versions 0.3.0–0.3.5 correct that design. For substantial whole-paper work, the writer reads the current assembled manuscript in order (preferably rendered), repairs cross-section contradictions and stitched-together prose, then optionally obtains one independent scholarly cold reading when available, permitted, and useful. That reader reconstructs the argument from the manuscript and offers a few demonstrable communication corrections. The writer implements and checks those corrections without automatic new reviews. Small edits get proportionate local reading. No score or acceptance threshold governs ordinary editing; optional legacy formal-run validators retain their record schema only when explicitly selected.

Literature discovery, empirical design, data work, and formal referee-response planning remain separate tasks. A manuscript revision supplies no authorization to reopen them.