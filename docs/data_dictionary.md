# Data layers and interpretation

All upstream population identifiers are preserved. `Year` is an upstream vintage label, not an authenticated effective date. `File` can represent a policy, form, campus document or OCR unit. A document key is the ordered triple Institution, Year, File. IDs beginning `p1r` identify the one-based data row of the immutable original CSV (excluding its header). SHA-256 values refer to exact UTF-8 sentence text unless explicitly labeled normalized.

| Output | Unit and permitted interpretation |
|---|---|
| frozen_observed_population.csv | 480 directly observed institution-years; sentence/candidate/file counts |
| document_provenance.csv | 518 institution-year-file keys; hashes, segmentation anomalies, duplicate diagnostics; full-vintage context remains unverified |
| sentence_index.csv (local) | Stable row IDs and source-text hashes; reconstruct with pipeline |
| provisional_clause_features.csv | All 87,159 included rows; Boolean regex features only; no legal adjudication |
| observed_category_mentions.csv | Institution-year lexical presence, pooling its files; no ownership inference |
| observed_vintage_pairs.csv | 330 adjacent observed pairs, gap, bundle-size and textual-overlap diagnostics |
| category_mention_pairs.csv | 330 pairs × nine categories; before, after and their difference |
| lexical_transition_matrix.csv | Absent/present lexical transitions; each row sums to 330 |
| lexical_institution_weighted_changes.csv | Pair and equal-university means, conditional bootstrap intervals |
| legal_identification_bounds.csv | No full-record adjudication; [0,1] unconstrained population bounds, not estimated confidence intervals |
| illustrative_legal_evidence.csv | 15 row links to 12 selected AI-assisted readings; multiple relationship fields separated by a vertical bar; no human reference standard |
| ownership_transition_review.csv | Actual textual comparisons, including their unresolved legal direction; not a validated transition matrix |
| validation_sample_manifest.csv | Probability sample, original-screen stratum and inclusion probability |
| validation_annotation_template.csv | Empty fields for genuine future annotations; pipeline regenerates it, so save completed annotations separately |
| embedded_url_inventory.csv | References visible in sentences, not a reconstructed original-source manifest |
| policy_source_snapshot.json (data/) | Frozen bytes/hashes and retrieval outcomes underlying selected readings |
| embedded_source_retrieval_log.json | Current link-recovery attempts; HTTP success is neither source correspondence nor historical authentication |

Knowledge flags may overlap. `emerging_technologies` includes AI and older mask-work/semiconductor terms; it is only a search dictionary. `patentable_inventions` also matches generic invention/patent wording and cannot establish patentability. Broad publication/book/article expressions can retrieve references rather than scholarly-work rules. These tradeoffs are disclosed; none of the flags are validated outcome labels.

Missing legal labels mean unknown, never no ownership. No source text is changed to repair duplicates or date discrepancies. Sensitivity files identify alternative populations explicitly. Each analysis uses direct observations; the carried-forward panel is read only to reconcile identifiers and counts.

`validation_supplement_manifest.csv` is a separate category/operation enrichment sample. Rows are sentence–stratum memberships, may overlap, and report within-stratum probabilities only; do not pool them unweighted with the main probability sample.

## Substantive comparison extension

- `substantive_relationship_changes.csv`: 13 curated relationship rows; before/after interpretation, excerpt, section, row IDs, URLs, source hashes, direction and qualifications. Excerpts are from the frozen cleaned corpus.
- `substantive_evidence_links.csv`: one relationship/endpoint/sentence link, preserving original institution, year, filename and text hash.
- `substantive_pair_classification.csv`: two selected endpoint pairs; adjacency, authentication, scope, definition/enumeration and mixed conclusions.
- `substantive_comparability_register.csv`: all 330 adjacent pairs; unreviewed cases remain unknown.
- `substantive_analysis_summary.json`: distinct counts of relationships, institutions, adjacent and nonadjacent comparisons; zero independently validated pairs.
- `revision_source_snapshot.json` under `data/`: frozen metadata for six reviewed context sources; raw documents stay local.
