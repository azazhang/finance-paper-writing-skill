# Architecture

## Design Goal

The capability is empirical-finance manuscript prose: an economically meaningful argument, decisive interpretable evidence, and natural authorial exposition. The skill guides editorial choices rather than attempting to certify them through a mandatory control system.

## Canonical Source

`skill/finance-paper-writing/` is the single substantive package. Provider installations point to or copy it, avoiding divergent instructions.

## Guidance and Optional Tools

The entrypoint makes the agent responsible for actually drafting the economic argument, including introduction and contribution when assigned, using the author's established evidence and direction. It contains the central standard, proportionate revision guidance, and routes to relevant references. The anti-defensive and finance-register references govern the actual prose. For GPT-family models and Codex, anti-defensive guidance is mandatory on **every** revision, including small edits; when model identity is unknown, apply it. Agents confirmed to be neither may treat it as a conditional reference. The authorial-voice reference is conditional on available author-approved prose or a voice-sensitive assignment; it uses existing examples without requiring a new profiling stage. The text-measure module is conditional; ordinary finance papers do not inherit classifier terminology.

The linter supplies optional diagnostic leads and uses the LaTeX manuscript-hash utility. The initializer is executable because it creates a run directory, template files, pass records, and manuscript metadata; it defaults to full-manuscript mode. The strict run-state validator checks that optional structured package. Legacy section-revision and prose-audit modes remain available for existing records. These tools are optional; the author or agent edits ordinary prose directly. Their pass/fail results measure conformity to a record format, not argument quality or publication readiness.

Earlier mandatory artifact and repeated-review requirements encouraged process to displace the requested revision. Versions 0.3.0–0.3.2 correct that design: use the current evidence, implement the requested change, check changed claims and rendering, and stop when the substantive task is fulfilled. Independent reading is bounded and task-driven, subject to current user and project restrictions.

Literature discovery, empirical design, data work, and formal referee-response planning remain separate tasks. A manuscript revision supplies no authorization to reopen them.