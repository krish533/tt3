#!/usr/bin/env python3
"""Candidate ownership-clause extraction. NOT a legal rights classifier."""
import argparse
from pathlib import Path
import re
import pandas as pd

CATEGORIES = {
"inventions": r"\b(?:inventions?|patent(?:able|s|ed)?)\b",
"software": r"\b(?:software|source code|computer programs?|algorithms?)\b",
"data": r"\b(?:research data|data ?sets?|databases?|data ownership)\b",
"scholarly": r"\b(?:scholarly works?|scholarly publications?|books?|manuscripts?)\b",
"teaching": r"\b(?:course materials?|lecture notes?|teaching materials?)\b",
"tangible": r"\b(?:biological materials?|tangible research property|cell lines?)\b",
"ai": r"\b(?:artificial intelligence|machine learning|generative AI|AI.generated)\b",
}
RULES = {
"university_claim": r"\b(?:university (?:shall )?own|owned by the university|property of the university|institutional ownership|title shall vest)\b",
"assignment": r"\b(?:shall assign|hereby assigns?|assignment of|assign(?:ed)? to|shall vest)\b",
"creator_retention": r"\b(?:retain(?:s)? ownership|owned by (?:the )?(?:faculty|author|creator|student)|faculty ownership)\b",
"exception": r"\b(?:except(?:ion)?|exclud(?:e|ed|ing)|unless|notwithstanding|shall not apply)\b",
"resources": r"\b(?:substantial use|significant use|university resources|scope of employment)\b",
"future_scope": r"\b(?:including but not limited to|without limitation|now known or hereafter|any and all)\b",
"approval": r"\b(?:prior written approval|subject to approval|must obtain approval)\b",
}
def run(source, outdir, start_year=1944, end_year=2025):
    df=pd.read_csv(source, low_memory=False)
    required={"Institution","Year","Sentence_Cleaned"}
    if required-set(df): raise ValueError("Missing: "+str(required-set(df)))
    df["Year"]=pd.to_numeric(df["Year"],errors="coerce")
    df=df[df.Year.between(start_year,end_year)&df.Sentence_Cleaned.notna()].copy()
    for key,pattern in {**CATEGORIES,**RULES}.items():
        df[key]=df.Sentence_Cleaned.astype(str).str.contains(pattern,flags=re.I,regex=True,na=False)
    df["asset_match"]=df[list(CATEGORIES)].any(axis=1)
    df["rule_match"]=df[list(RULES)].any(axis=1)
    df["candidate"]=df.asset_match & df.rule_match
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    review=df[df.candidate].copy()
    for c in ["verified_source","rights_holder","legal_effect","trigger","exceptions","coder_notes"]:
        review[c]=""
    review.to_csv(out/"ownership_clause_manual_review_queue.csv",index=False)
    counts=df.groupby(["Institution","Year"],dropna=False).agg(
       sentences=("Sentence_Cleaned","size"),candidates=("candidate","sum")
    ).reset_index()
    counts.to_csv(out/"observed_document_candidate_counts.csv",index=False)
    print("Observed institution/year text groups:",len(counts),"Candidate sentences:",len(review))
    return counts,review
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("csv");p.add_argument("--outdir",default="results")
    p.add_argument("--start-year",type=int,default=1944);p.add_argument("--end-year",type=int,default=2025)
    a=p.parse_args();run(a.csv,a.outdir,a.start_year,a.end_year)
