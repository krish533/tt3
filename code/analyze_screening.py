#!/usr/bin/env python3
"""Denominator-aware descriptive analysis. Flags are NOT legally validated rights."""
import argparse
from pathlib import Path
import pandas as pd
FLAGS="inventions software data scholarly teaching tangible ai university_claim assignment creator_retention exception resources future_scope approval".split()
def analyze(queue,counts,outdir):
 x=pd.read_csv(queue); d=pd.read_csv(counts); p=Path(outdir);p.mkdir(parents=True,exist_ok=True)
 for c in FLAGS:x[c]=x[c].astype(bool)
 x["decade"]=(x.Year//10*10).astype(int);d["decade"]=(d.Year//10*10).astype(int)
 tab=d.groupby("decade").agg(documents=("Institution","size"),institutions=("Institution","nunique"),sentences=("sentences","sum"),candidates=("candidates","sum")).reset_index()
 tab["per_1000_sentences"]=(1000*tab.candidates/tab.sentences)
 for c in FLAGS:
  v=x.groupby("decade")[c].sum()
  tab[c+"_matched_sentences"]=tab.decade.map(v).fillna(0).astype(int)
 tab.to_csv(p/"screening_by_decade.csv",index=False)
 versions=d.groupby("Institution").agg(observed_versions=("Year","nunique"),first=("Year","min"),last=("Year","max")).reset_index()
 versions.to_csv(p/"institution_historical_coverage.csv",index=False)
 for c in ["university_claim","creator_retention","future_scope","assignment","exception"]:
  sample=x[x[c]].sample(n=min(15,int(x[c].sum())),random_state=2031)
  sample[["Institution","Year","File","Sentence_Number","Sentence_Cleaned"]].to_csv(p/("review_sample_"+c+".csv"),index=False)
 print(tab[["decade","documents","institutions","sentences","candidates","per_1000_sentences"]].to_string(index=False))
 print("Institutions with multiple observed vintages:",(versions.observed_versions>1).sum())
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--queue",default="results/ownership_clause_manual_review_queue.csv");ap.add_argument("--counts",default="results/observed_document_candidate_counts.csv");ap.add_argument("--outdir",default="results");a=ap.parse_args()
 analyze(a.queue,a.counts,a.outdir)
