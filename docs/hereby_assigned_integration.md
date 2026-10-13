# Hereby Assigned — integration and citation-verification workstream

Date: 2026-10-13
Status: In progress. This branch preserves the existing `tt3` manuscript, which is a separate, more cautious study titled *Who Owns Academic Knowledge?* Do not replace `manuscript/main.tex` or `overleaf/main.tex` with *Hereby Assigned* without a comparative reconciliation.

## Source versions
- Current remote repo: `krish533/tt3`; canonical paper `manuscript/main.tex`, Overleaf mirror `overleaf/main.tex`.
- Locally revised *Hereby Assigned*: `~/hereby-assigned/main.tex` and `~/hereby-assigned/references.bib` according to the author's 2026-10-13 terminal log. Not uploaded to this branch yet. The separately uploaded *Hereby Assigned* PDF remains the older 12-page draft.
- Local audit outputs mentioned in that log: `~/hereby-assigned/docs/final_citation_audit.csv`, `unresolved_claims.md`, `literature_gap_review.md`; read these before reconciling.

## Required literature and claim corrections
1. State novelty narrowly: Halilem et al. (2017) and Jamali (2024) already study multidimensional university IP policies. Emphasize repeated U.S. policy vintages and within-university combinations of objects, covered people, assignment mechanisms, and creator protections.
2. Separate *Stanford v. Roche* (Supreme Court 2011: Bayh–Dole does not automatically vest title) from Stanford v. Roche (Federal Circuit 2009: promise-to-assign vs present-assignment drafting). Use original decisions, and interpret the 2011 uptake as temporal association rather than causal proof.
3. Distinguish lexical mentions (software, data, course material) from affirmative ownership rules, exclusions, and administrative procedures. Avoid calling mention counts changes in enforceable rights.
4. Qualify Owen-Smith and Powell (2001): institutional incentives and disclosure choices, not directly estimated effects of broad ownership clauses.
5. Describe the 2018 NIST federal-contract assignment rule accurately; relocation into standalone assignment agreements remains a hypothesis without direct documentation.
6. The joint addition of ownership language and creator carve-outs is an observed association; faculty bargaining as a mechanism is speculative absent minutes, interviews, or governance documents.
7. Restrict AI-silence claims to the observed 45 records from 2023–2025 and the specific search patterns, not all U.S. universities.
8. Rerun all regressions and audit plotted labels with the source archive and scripts before changing reported point estimates.

## Source pointers (verification is NOT fully complete)
- Halilem et al. (2017): https://doi.org/10.1016/j.respol.2017.07.002
- Jamali (2024): https://doi.org/10.1371/journal.pone.0304647
- Owen-Smith & Powell (2001): https://doi.org/10.1023/A:1007892413701
- U.S. Supreme Court, *Stanford v. Roche*: https://supreme.justia.com/cases/federal/us/563/776/
- U.S. Federal Circuit (2009): https://law.justia.com/cases/federal/appellate-courts/cafc/08-1509/08-1509-2011-03-27.html
- NIST Bayh–Dole guidance: https://www.nist.gov/tpo/policy-coordination/bayh-dole-act/2018-faqs
- U.S. Copyright Office AI reports: https://copyright.gov/policy/artificial-intelligence/

## Next integration steps
- Commit the actual, latest locally revised `~/hereby-assigned/main.tex`, `references.bib`, and audit files into a NEW subdirectory `hereby-assigned/` on this branch (not over `tt3/manuscript/`).
- Compare its claims against `tt3/docs/substantive_revision_audit.md`, `tt3/references/reference_audit.csv`, and the 13 source-linked Utah/Hawaiʻi comparisons.
- Resolve disagreements with source links and reproducible outputs; preserve both versions and annotate what is still uncertain.
- Once reconciled, create an isolated Overleaf import ZIP using the `hereby-assigned/` LaTeX sources and figures.
