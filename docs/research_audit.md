# Current revision

The 11 October substantive revision supersedes the manuscript and artifact status below. See [substantive revision audit](substantive_revision_audit.md) for the new comparisons, 54-source bibliography, four tables, 20-page manuscript and current limitations. Original corpus findings below are unchanged.

# Paper 3 research audit — 10 October 2026

## What this release establishes

The supplied dataset and original screening counts are reproducible. The available corpus has 87,159 included cleaned sentences from 150 universities and 480 observed institution-years, 1944–2025. The original 87,160-row input has one 1925 row outside the established sample. The panel reconciles exactly: 480 direct observations plus 3,797 carried-forward rows equals 4,277 institution-years. Original regex screening returns 2,779 candidates in 449 observed records. These counts are not numbers of university-owned inventions or authenticated legal instruments.

The analytical population is frozen at upstream commit `25a9472b34334825b6d6c6a334f5b88eb00695b5`. The sentence file SHA-256 is `92a7d153f630de78c973fc0b8915c5860b0a87320194781c73eca9601b3d3aec`; the panel hash is `694c21acc07d2a50ed27199d0e7ec01bb6974f08f843cbce2d7da4318f864198`. No Paper 1 or Paper 2 file was changed.

## Documentary findings

There are 518 institution-year-file keys but only 475 distinct filenames. Twenty-nine observed institution-years have multiple files. Some contain forms or campus-specific policies, so file count is neither document independence nor revision count. Georgia Tech has 3,662 rows participating in nonunique sentence-number keys (1,831 beyond the first occurrence). Stable row IDs prevent these collisions from merging distinct text. Exact raw-row duplication is zero. Within-document normalized sentence duplication is 2,703 rows. Fifteen document groups participate in exact normalized-text duplication, including shared system policies. Delaware 1993 and 2008 have identical normalized sentence sets. These observations remain in the primary population; sensitivity results are separate.

One VCU 2021-labelled record has a filename containing 2027. This is reported without silently relabeling it. The shortest cleaned sentence has 48 characters, which cautions against assuming short headings or clauses were preserved by the upstream cleaning. Urbanicity has missing values, but it is not used in the legal or historical analysis. The missing-value and identifier tables retain details.

Historical coverage is highly uneven; there are no 1950s observations. The 330 adjacent observed pairs come from 129 universities. Thirty-five pairs change file counts. These are endpoint comparisons, not a complete sequence of authenticated revisions. No carried-forward years enter the transition analysis.

## Source recovery and legal readings

The first selected-source pass attempted seven URLs: six downloaded and one old Creighton guide failed TLS hostname validation. Sources include Illinois State's official 2024 page, an undated contextual handbook, Wake Forest's earlier reprint and 2017 Reynolda policy, Creighton's 2019 policy, and Palmer's 1962 historical survey. The earlier Wake Forest reprint bears a 2006 amendment and cannot authenticate pristine 1999 wording. Palmer corroborates Caltech's historical allocation architecture but differs from the cleaned corpus in modal language. Numbered cross-references in Illinois State require caution. Wake Forest's companion copyright policy remains unverified for the relevant vintage.

A systematic supplementary inventory found 295 visible URL occurrences and 212 cleaned unique URLs in the included corpus. Thirty-nine plausible .edu policy links were attempted: 19 returned content and 20 failed. These are references embedded in policy sentences, not necessarily the sources of those sentences. Several successful links lead to portals, login pages or identical redirected content. They remain `downloaded_unreviewed`, never source-authenticated. All attempts and hashes are retained; full downloaded documents stay local.

Twelve selected AI-assisted readings are linked to 15 corpus rows, source sections and frozen retrieval hashes. The full policy context was checked for the selected relationships where available, with missing companions and vintage problems recorded. These are defensible provisional textual interpretations, not independent expert validation, an exhaustive legal dataset or evidence of enforceability. The primary document-provenance table retains context-unverified status for full-document adjudication; a selected section match does not upgrade the whole institution-year.

## Analysis and validation

The original screen misses actual operative wording using defined terms or different verb forms. It misses the inspected Wake Forest assignment introduction, Illinois State's normal-ownership wording, and Creighton's reciprocal license and some exceptions. The expanded review queue contains 25,168 sentences, including 22,722 not selected by the original screen. It is broader, not a validated improvement in accuracy. Candidate status also does not mean a university claim: exceptions and resource language can match. Purposive diagnostics do not yield population false-positive/false-negative rates.

The lexical matrices have nine categories and 330 pairs each. Research-data appearances/disappearances are 57/24; software 48/27. University-weighted means are about 0.104 and 0.055 respectively. Restricting gaps to ten years yields 233 pairs from 97 universities, with means about 0.050 for data and -0.008 for software. The latter sensitivity weakens a general software-expansion narrative even at the lexical level. Bootstrap intervals are conditional on observed institutions and do not incorporate nonrandom archive selection, shared-system dependence or semantic uncertainty.

The probability validation sample has 178 sentences from 68 institutions, stratified by decade and original-screen status, seed 2031. It includes negative examples and known inclusion probabilities. Category coverage is reported. A separate enrichment sample supplies 240 stratum draws (236 distinct sentences from 80 institutions) across 20 category/operation dictionaries, with within-stratum probabilities and overlapping membership preserved. Actual category precision remains unknown. No independent human coder or reference-standard labels were available. Precision, recall and agreement are null. No fully adjudicated institution-year outcomes exist; [0,1] bounds denote lack of identification, not estimated uncertainty around a point estimate.

## Literature, writing and artifacts

The manuscript is rewritten as an evidence-limited article rather than a claim of universal ownership expansion. It separates definitions, title, assignment, retained use, exceptions and enforceability; addresses competing economics and legal interpretations; and acknowledges close prior empirical studies. All 48 bibliography entries resolve and are cited. The reference audit preserves primary links, relevant claims, corrections and access limits. Most scholarly sources were checked through metadata plus primary abstracts/summaries, not exhaustive independent full-text review.

Six tables and one figure are generated or explicitly tied to the evidence ledger. Numerical and citation audits accompany them. The PDF compiles with standard packages and was visually reviewed. The canonical LaTeX is mirrored byte-for-byte into a self-contained Overleaf project with a checksum manifest and deterministic import ZIP. No online project was created or overwritten.

The journal accepts RTF as a Word submission format. The RTF export preserves the article, tables, figure and bibliography, and its decoded text was checked. It has not been rendered in Word. The bundled document-rendering runtime required for DOCX proofing was not exposed in this execution environment; the user's desktop renderer was not substituted. A rendered DOCX is therefore not claimed. The RTF requires external pagination review before submission.

## Remaining risks and release decision

The broad empirical question is not complete. The essential missing evidence is authenticated historical context and independent qualified coding of comparable rights relationships. Paid services were not purchased, and lack of a subscription was not treated as license to fabricate validation. Missing author declarations and Word pagination also prevent a submission-ready designation. The adversarial review concludes that the archive audit and provisional manuscript are useful but that a referee could reasonably reject the legal-historical contribution as incomplete. The release preserves that conclusion explicitly.

## Execution verification

A clean Git checkout at `d2cb7f1` fetched the two immutable source files over verified TLS, reproduced the pipeline, passed 13 tests and matched all 37 recorded output checksums without tracked-file changes. A macOS certificate-store issue found during this test was fixed by using the pinned certifi CA bundle; certificate checking was never disabled. The test reused the installed pinned Python environment rather than provisioning a new virtual environment. The Overleaf import ZIP compiled independently without network access. All 18 pages of the final PDF were visually reviewed, with no unresolved references or overfull boxes. RTF decoded text contains 6,479 whitespace-delimited words; the manuscript reports an approximate 6,500-word total. These checks verify implementation and artifacts, not legal accuracy.

The public GitHub Actions replication workflow also completed successfully for `d2cb7f1`: https://github.com/krish533/tt3/actions/runs/38116847669 (checked 11 October 2026). This independently exercised the pinned installation and analysis workflow on the configured Ubuntu/Python 3.14 runner.
