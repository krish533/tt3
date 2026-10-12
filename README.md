# Who Owns Academic Knowledge?

Paper 3 studies university property-right allocations, separately from Paper 1's policy-communication analysis and Paper 2's commercialization study. This release is an **audited research package and evidence-limited manuscript, not a submission-ready validated legal study**.

The original counts reproduce: 150 universities, 480 directly observed institution-years (1944–2025), 4,277 panel rows including 3,797 carried-forward rows, and 2,779 screening matches in 449 observed records. The audit distinguishes 518 institution-year-filename groups. It preserves the established population, excludes the single 1925 row, and identifies repeated text, sentence-key collisions and multi-file records.

Across 330 adjacent observed-vintage pairs from 129 universities, data terminology appears in 57 pairs and disappears in 24; software appears in 48 and disappears in 27. These are **mentions, not ownership transitions**. Software results are sensitive to restricting the gaps between vintages. The substantive revision adds 13 source-linked relationship comparisons at Utah and Hawaiʻi, alongside the earlier illustrative readings. Utah combines changed assignment wording with a narrower resource branch; Hawaiʻi preserves a qualified creator baseline while specifying use rights, with an earlier contractual precedent. These are purposive comparisons, not national frequencies. See [the substantive scientific audit](docs/substantive_revision_audit.md). There are no independent human annotations or fully adjudicated institution-year outcomes.

## Read the paper and audit

- [Canonical LaTeX](manuscript/main.tex), [compiled PDF](deliverables/paper3.pdf), [Word-compatible RTF](deliverables/paper3-word.rtf)
- [Overleaf import ZIP](deliverables/paper3-overleaf.zip); no online project was created
- [Research audit](docs/research_audit.md), [adversarial review](docs/adversarial_review.md), [submission readiness](docs/submission_readiness.md)
- [Legal codebook](docs/legal_coding_protocol.md), [data dictionary](docs/data_dictionary.md)
- [54-entry reference audit](references/reference_audit.csv), [BibTeX](references/references.bib), [verification limits](docs/reference_verification_notes.md)

## Reproduce

Install Python 3.14 and `requirements.txt`, then run:

```sh
python3 code/replicate.py
```

For the PDF, install Tectonic 0.17.0 and use `python3 code/replicate.py --pdf`. See [replication instructions](replication/README.md) for immutable source downloads, offline operation, optional policy retrieval, build requirements and interpretation limits. Raw text and downloaded policies are not newly redistributed; local reconstructed review text is regenerated from the pinned original source.

All new work remains in this repository. Papers 1 and 2 were inspected through read-only local copies and were not modified. The principal remaining requirement is authenticated source-context coding with a credible independent legal reference standard. The package deliberately leaves unavailable precision, recall and agreement statistics blank.
