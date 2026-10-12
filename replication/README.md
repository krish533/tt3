# Reproducing Paper 3

Use Python 3.14 and the pinned packages in `requirements.txt` (the execution environment used Python 3.14). The deterministic analytical command is:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 code/replicate.py
```

Run from the repository root. The first run downloads two files from the immutable Paper 1 commit and refuses incorrect SHA-256 values. If network access is unavailable, obtain those exact files using `data/source_manifest.json`, place them under `input/`, and rerun. Alternatively `python3 code/fetch_sources.py --upstream /path/to/read-only/Tech-transfer-1` copies the two files without modifying that checkout. Subsequent analysis runs are offline. Approximately a few minutes and less than 1 GB of free disk are sufficient in the tested environment; reconstructed context and uncompressed derived files consume most space.

The pipeline reproduces the original screen, audits identifiers/population, constructs provisional flags, analyzes direct-vintage pairs, regenerates the sample and illustrative evidence ledger, inventories embedded URLs, builds the bibliography/tables, checks citations, exports RTF and the Overleaf mirror, and runs the tests. It does not manufacture a human reference standard. Save genuine future annotations outside the regenerated blank template.

## PDF and Overleaf

Install Tectonic 0.17.0, then run `python3 code/replicate.py --pdf` (or `make paper`). Tectonic fetches standard packages on first use; compilation is offline after its cache is populated. The PDF is copied to `deliverables/paper3.pdf`. Alternatively unzip `deliverables/paper3-overleaf.zip` into a new Overleaf project, select `main.tex` and XeLaTeX. Paths are relative and no shell escape or custom fonts are required. The Times-family font is supplied by standard LaTeX packages.

Edit only `manuscript/main.tex`, generated-table code, or the accepted reference inputs. `python3 code/sync_overleaf.py` regenerates the mirror and ZIP; `--check` fails on divergence. LaTeX and RTF are generated from the same master and data, but RTF is not yet certified for Word pagination. PDF visual QA uses Poppler: `pdftoppm -png deliverables/paper3.pdf build/pages/page` after creating the output directory. Tectonic binary/TeX cache and PDF metadata can vary across environments; compare numerical CSVs rather than require cross-platform identical PDF bytes.

## Optional source and reference recovery

`python3 code/retrieve_policy_sources.py` retrieves the selected official policies and historical survey. `python3 code/recover_embedded_sources.py --fetch` attempts plausible .edu policy links found inside the corpus (HTTPS, time/size limits, four concurrent requests). These links may reference other documents, redirect to portals or fail; HTTP 200 is never source authentication. Poppler `pdftotext` is needed for PDF context extraction. Downloads stay in ignored `input/`. The original reviewed snapshot is frozen in `data/policy_source_snapshot.json`; changed cached bytes cause evidence rebuilding to fail until readings are re-reviewed. Retrieval logs include errors and current hashes.

`python3 code/verify_reference_metadata.py` retrieves missing Crossref metadata caches. It does not validate substantive claims or automatically accept title-search matches. `build_references.py` contains the accepted corrections and produces the BibTeX and author-date display bibliography. Review `references/reference_audit.csv` before treating any source as fully read.

## Sharing and audit

The package redistributes derived identifiers, flags, counts and short analytical paraphrases, not the upstream full corpus or downloaded policies. Public accessibility does not establish unrestricted republication rights. Original-text validation samples and reconstructed context are rebuilt locally. `results/table_figure_audit.csv` and `results/manuscript_claim_audit.csv` connect manuscript claims to outputs. `docs/data_dictionary.md` distinguishes the units. `docs/submission_readiness.md` and `docs/adversarial_review.md` record unresolved research and publication requirements.

## Previous release verification (superseded for current artifact hashes)

A fresh Git checkout at `d2cb7f1` downloaded the pinned inputs and completed the pipeline with 13 tests passing. All 37 recorded deterministic output hashes matched, and the checkout remained clean. This used the existing pinned Python environment, not a newly provisioned virtual environment. The exported Overleaf ZIP also compiled independently using only the cached TeX bundle. See `verified_run.txt`, `execution_environment.json`, and `results/release_verification.json`. Run `python3 code/package_release.py --check` to check recorded output hashes; `python3 code/package_release.py` refreshes the replication ZIP after approved changes.

## Substantive revision extension (11 October 2026)

`python3 code/replicate.py` now also runs `analyze_substantive_transitions.py`. This regenerates curated relationship comparisons and their evidence links from `data/substantive_comparisons.json`, validates original row identities/excerpts and generates the complete adjacent-pair comparability register. Interpretive labels are research inputs, not algorithmically proven legal findings. Six contextual source hashes are frozen in `data/revision_source_snapshot.json`; any available cached file must match. The deterministic pipeline does not require redistribution or renewed download of those documents.

`python3 code/retrieve_revision_sources.py` optionally retrieves the official context documents into ignored `input/revisions/`, with TLS verification, hashes and failures logged. Poppler is required for PDF extraction. The legislative-history DOCX is read as XML for research context, not converted into a submission artifact. A changed source hash requires renewed review before changing the snapshot. The 2009 agreement URL currently fails; the separately listed 2003 agreement supplies the reviewed contractual precedent.

The 13 relationship entries are nested in two institutional comparisons, not 13 independent revisions. Only Utah belongs to the original adjacent-pair register. Hawaiʻi spans an intermediate unverified vintage and must not be pooled into the 330-pair denominator. Independent human legal validation remains absent.

Current revision verification: a clean local clone of `4e5693929de12c5a75cb0ccb104de08c402a29f4` completed the extended pipeline with 15 tests passing, all 43 recorded output hashes matching and no working-tree changes. Immutable input files were copied from the read-only upstream clone and checksum-verified; the installed pinned Python environment was reused. The Overleaf ZIP independently compiled using cached TeX only. The PDF contains 20 visually inspected pages; decoded RTF text contains 7,462 whitespace-delimited words. These checks do not certify legal interpretations or Word pagination.

GitHub Actions also completed successfully for the substantive code/manuscript commit `4e5693929de12c5a75cb0ccb104de08c402a29f4`: https://github.com/krish533/tt3/actions/runs/38212890923. The subsequent audit-only commit records these results and updates the replication archive.
