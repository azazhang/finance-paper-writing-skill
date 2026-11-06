# Finance Paper Writing Skill

A compact Agent Skills package for writing and revising research manuscripts in **financial economics**. Its standard is a compelling economic argument, credible and interpretable evidence, and scholarly finance publication prose.

The writing agent develops the requested abstract, introduction, results interpretation, contribution, or complete manuscript. For substantive full-paper work, it reads the assembled paper and repairs inconsistencies before any optional independent cold reading. GPT-family models and Codex must apply the anti-defensive-prose guidance on **every** finance-manuscript prose edit, including proofreading a sentence.

## Package

- [SKILL.md](skill/finance-paper-writing/SKILL.md): core writing instructions, guidance routing, and required agentic manuscript review.
- [Voice calibration](skill/finance-paper-writing/references/voice-calibration.md): finance-journal publication conventions, with six annotated published exemplars.
- [Editorial diagnostics](skill/finance-paper-writing/references/editorial-diagnostics.md): concrete agentic recognition and repair of development-language leakage, research-memo writing, generic AI rhetoric, patchwork passages, and miscalibrated claims.
- [Anti-defensive prose](skill/finance-paper-writing/references/anti-defensive-prose.md): calibrated claims and natural academic argumentation; mandatory for GPT/Codex.
- [Evidence and claims](skill/finance-paper-writing/references/evidence-and-claims.md): quantitative interpretation, exhibit selection, attribution, and inferential boundaries.
- [Independent reader](skill/finance-paper-writing/references/independent-reader.md): the writing agent's assembled-manuscript reading and one bounded optional fresh reading.
- [Closest-paper positioning](skill/finance-paper-writing/references/closest-paper-positioning.md) and [text measures](skill/finance-paper-writing/references/text-measure-papers.md): consult for relevant writing tasks.
- [Original illustrative passages](skill/finance-paper-writing/examples/model-passages.md): optional synthetic examples.

**Manuscript validation is agentic.** The agent reads and repairs the actual scholarly manuscript against these instructions and the source evidence. The package contains no keyword scanner, programmatic manuscript validator, scoring system, reviewer-run harness, mandatory review forms, or writing-compliance certificates.

## Install

The **only executable tool** retained in this repository is the local installer:

```bash
python3 scripts/install_local.py --providers agents,codex,claude,cursor
```

Installations use symlinks by default, keeping local agents current with the canonical skill. The installer supports `--dry-run` and managed copies via `--mode copy`; it protects existing unrecognized installations and modified copies. For other agents, use their verified Agent Skills discovery directory. The standalone Gemini App manages account-level skills separately from Mac-local agent installations.

The full history of older programmatic tooling remains in Git revisions preceding v0.4.0. The active package contains writing guidance and examples, plus the installer.