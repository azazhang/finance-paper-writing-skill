# Architecture

## Design Goal

The repository is a finance-prose control workflow, not another collection of generic writing suggestions. It must remain useful when other academic-writing skills are installed but fail to trigger or fail to govern a long manuscript task.

## Canonical Source

`skill/finance-paper-writing/` is the only substantive skill package. Codex, Claude Code, and Cursor installations point to or copy this same directory.

No provider-specific copy is maintained in the repository. This prevents silent divergence between adapters.

## Enforcement Layers

1. **Trigger description**  
   The frontmatter names common finance-manuscript requests and failure symptoms.

2. **Visible activation**  
   Manuscript-level work begins by naming the skill and initializing a run.

3. **Persistent artifacts**  
   Charter, ledgers, audits, pass records, and reviewer reports make adherence inspectable.

4. **Pass separation**  
   Each pass has one objective, a recorded role, an artifact, and a coherent input/output hash chain.

5. **Independent review**  
   The lead writer cannot supply the only acceptance review.

6. **Hash freshness**  
   Reviews and lint results apply only to the composite state of the main TeX file and recursively included sources that they examined.

7. **Deterministic verification**  
   Scripts catch recognizable leaks and incomplete run state.

8. **Judgment gate**  
   A cold reader supplies evidence-backed ratings on eight prose dimensions. Static checks cannot replace this step.

## Scope

The universal core covers empirical finance prose, evidence ordering, closest-paper positioning, reader context, author voice, and caveat discipline.

Design-specific material belongs in optional references. The repository currently contains one such module for text-based measures. Loading that module is conditional; it does not change the core requirements for ordinary corporate-finance, asset-pricing, banking, or household-finance papers.

## Companion Skills

Literature review, bibliography validation, formal proofreading, LaTeX compilation, PDF inspection, and referee-response planning remain separate capabilities. The pass log records whether they were actually invoked. Their installation alone does not satisfy this workflow.
