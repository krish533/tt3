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

## Verified execution

A fresh Git checkout at `d2cb7f1` downloaded the pinned inputs and completed the pipeline with 13 tests passing. All 37 recorded deterministic output hashes matched, and the checkout remained clean. This used the existing pinned Python environment, not a newly provisioned virtual environment. The exported Overleaf ZIP also compiled independently using only the cached TeX bundle. See `verified_run.txt`, `execution_environment.json`, and `results/release_verification.json`. Run `python3 code/package_release.py --check` to check recorded output hashes; `python3 code/package_release.py` refreshes the replication ZIP after approved changes.
