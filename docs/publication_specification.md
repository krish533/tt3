# WP3 publication specification — Science and Public Policy

Target (provisional): *Science and Public Policy* (Oxford University Press).
Current journal source: https://academic.oup.com/spp/pages/author-guidelines

## Editorial and submission constraints
- Main article 8,000–10,000 words **including title, abstract, tables, graphs, references**, per current guidelines. Verify again at submission.
- Abstract <=150 words; one clear question, design, main validated finding, contribution.
- Journal currently requests Word (.doc/.docx/.rtf) for submission. Overleaf/LaTeX is the authoring master, not sufficient as the final submission format. Produce a polished Word conversion and compare it line-by-line with the PDF.
- Journal currently describes Oxford HUMSOC bibliography style, with references in alphabetical order. Follow **the current author-guidelines page** rather than conflicting archived instructions.
- Short headings, ordinary academic paragraphs, uncluttered tables without vertical rules or colored shading. Keep precise institutional/legal terminology.
- Cite responsibly: factual claims need a source; include competing findings; separate federal law, university policy, contract interpretation and empirical conjecture.

## Manuscript voice
Write as an experienced empirical legal scholar and economist. Prefer natural argument and clear examples over formulaic AI scaffolding. Avoid repeated 'first', 'novel', 'importantly', 'in today's rapidly evolving landscape', 'delve', 'comprehensive', and invented mechanisms. No generic policy checklists or numbered-results structure unless needed. Use continuous prose, carefully qualified findings, institutional examples, and meaningful transitions. Do not fabricate research design, legal conclusions, authorities, coauthors or affiliations. Academic integrity matters more than AI-detector gaming.

## Literature: 40+ **verified relevant** sources, not filler
At least 40 if genuinely pertinent; no quota-based padding. Maintain `references/reference_audit.csv` with:
`citekey,authors,title,year,journal_or_publisher,volume,issue,pages,doi,verified_publisher_url,verification_date,substantive_relevance,claim_supported,checked_status`.
- Verify each article's exact metadata via DOI resolver and official journal/publisher listing (Crossref alone is insufficient for disputed facts). Book chapters and legal cases need authoritative publisher/court records.
- For each literature assertion, record which verified paper establishes it and whether it concerns university rules, statutory ownership, Bayh–Dole, faculty rights, data/software, technology transfer or empirical legal methodology.
- Remove mismatches, duplicate entries, phantom DOIs, and cited-but-unlisted items; ensure no irrelevant padding.
- Required thematic coverage: university IP evolution pre/post Bayh-Dole (including pre-existing institutional practices); economics of incomplete contracts/property rights; employee inventions and contractual assignment; Stanford v Roche and Bayh-Dole's limits; scholarly/copyright exceptions; research-data governance, material transfer, software and open science; university IP comparative empirical studies; policy diffusion/institutional isomorphism; legal-text methods and validation.
- Record competing explanations and substantive boundary cases; do not claim absence of prior work without a thorough search.

## Empirical tasks still needed before claiming completion
1. Confirm archival provenance of 480 policy-year records, check duplicate/inconsistent vintages, no carried-forward observations as unique documents.
2. Retrieve original entire source policies and surrounding paragraphs wherever possible.
3. Human-reviewed legal coding of ownership, assignment, creator-retained rights, nonownership, exceptions, triggering conditions; double-code stratified positive and negative samples; disclose precision, recall and agreement.
4. Distinguish underlying legal ownership from university assertions in their written policies; do not imply enforceability without legal review.
5. Version-linked within-university comparisons rather than naive 1940s vs 2020s composition; check period coverage.
6. Tables/figures compiled only from frozen validated dataset, complete provenance and reproducible code, seed and environment lock.
7. Independently reproduce all reported counts, legal-coding uncertainty and manuscript tables from a clean checkout. No claims beyond evidence.

## Deliverables
- `overleaf/main.tex` and all referenced tables and figures; Overleaf-compatible ZIP.
- `manuscript/main.tex` canonical version or a clearly documented symlink/copy strategy. Avoid divergence.
- `references/references.bib` plus `references/reference_audit.csv` with >=40 *verified and materially relevant* sources if attainable.
- A Word-format submission version after validation.
- `replication/README.md`, code, tests, data provenance, output checksums, coding audit and error log.
- `docs/submission_readiness.md` with each uncompleted item explicitly marked.

## Overleaf
According to https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/github-synchronization,
GitHub synchronization requires eligible Overleaf access. On Overleaf choose New Project > Import from GitHub > krish533/tt3 (if enabled). Note that Overleaf cannot link two pre-existing projects in that integration. Import only the `overleaf/` subtree as ZIP if repo project-size/files cause problems. Set main document to `overleaf/main.tex`.

No claim that Overleaf has been created or that manuscript is final until confirmed.
