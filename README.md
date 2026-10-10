# TT3 — Who Owns Academic Knowledge?

Independent Paper 3. Studies **rights allocation**, not PCI (Paper 1) or commercialization outcomes (Paper 2).

## Dataset
Canonical source: [Paper 1 replication repository](https://github.com/krish533/Tech-transfer-1), `P1_replication_package/data/raw/policy_sentences_cleaned_combined.csv`.
Verified Paper 1 primary panel: **1944–2025**, **150 universities**, **480 directly observed policy records** and **4,277 institution-year panel rows** (most carried forward). Never count carried-forward rows as new policy versions. Exclude 1925. The original raw data are not duplicated in this repo.

## Run
```bash
pip install pandas
python code/extract_ownership.py /local/path/to/policy_sentences_cleaned_combined.csv --outdir results
python -m unittest discover -s tests -v
pdflatex -interaction=nonstopmode manuscript/main.tex
```

**Status:** Synthetic-fixture test passes; LaTeX compiles. Full-data execution is **not completed** because the GitHub connector would not transfer the 29.5 MB raw CSV into the execution container. All legal coding and substantive findings remain pending.

The algorithm produces *candidates for human review*, NOT verified ownership outcomes. Before publication, check original paragraphs/source documents, verify institutional IDs and policy vintages, perform manual double coding plus negative-sample recall checks, and compare actual within-institution revisions. See manuscript for full protocol.
