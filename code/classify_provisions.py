"""High-recall review aids, explicitly NOT validated legal labels.

Keep lexical evidence separate from a legal relationship. A sentence can have
multiple flags; an institution name or an asset term does not identify a holder.
"""
import json
from pathlib import Path
import re
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
ASSETS={
    'patentable_inventions':r'\b(?:patents?|patentable|inventions?)\b',
    'software':r'\b(?:software|computer programs?|source code)\b',
    'algorithms':r'\balgorithms?\b',
    'research_datasets':r'\b(?:research data|data\s?sets?|databases?|data ownership)\b',
    'scholarly_publications':r'\b(?:scholarly|publications?|articles?|books?|dissertations?|theses)\b',
    'teaching_materials':r'\b(?:course\s?ware|course materials?|teaching materials?|instructional materials?|syllabi|class notes|lecture notes)\b',
    'biological_materials':r'\b(?:biological materials?|cell lines?|plasmids?|organisms?|DNA|RNA)\b',
    'tangible_research_property':r'\btangible research (?:property|materials?)\b',
    'emerging_technologies':r'\b(?:artificial intelligence|machine learning|generative AI|AI.generated|mask works?|semiconductor)\b'
}
OPERATIONS={
    'ownership_wording':r'\b(?:own(?:s|ership)?|owned|property of|title (?:to|in|shall)|vest(?:s|ed)?)\b',
    'present_assignment_wording':r'\b(?:hereby|thereby)\s+(?:assign(?:s|ed)?|transfer(?:s|red)?)\b',
    'assignment_obligation_wording':r'\b(?:(?:shall|must|will|agree(?:s)? to|required to)\s+(?:be\s+)?assign|assignment|assigned to)\b',
    'creator_retention_wording':r'\b(?:retain(?:s)? (?:all )?(?:rights|ownership)|(?:creator|author|inventor|student|faculty).{0,35}\bown(?:s|ership)?|property of (?:the )?(?:individual|inventor|creator))\b',
    'nonexclusive_license_wording':r'\bnon[ -]?exclusive\b',
    'exclusive_license_wording':r'(?<!non-)(?<!non )\bexclusive licen[sc]e\b',
    'exception_wording':r'\b(?:except(?:ion|ions)?|unless|exclud(?:e|ed|es|ing)|shall not apply|not subject to)\b',
    'waiver_wording':r'\b(?:waiv(?:e|er|es)|releas(?:e|es) (?:its |the )?rights|relinquish)\b',
    'procedure_wording':r'\b(?:disclos(?:e|ure)|report|submit|appeal|committee)\b',
    'definition_wording':r'\b(?:defined|definition|means|includes?|refers to)\b',
    'negation_wording':r'\b(?:not|no|neither|without)\b'
}
TRIGGERS={
    'employment':r'\b(?:employment|employee|line of duty|job responsibilities)\b',
    'sponsored_funding':r'\b(?:sponsor(?:ed)?|grant|federal funds|funding agreement)\b',
    'resources':r'\b(?:substantial use|significant use|incidental use|university resources|university funds|institute facilities)\b',
    'commission':r'\b(?:commissioned|specifically directed|institutional works?|work.for.hire)\b',
    'affiliation':r'\b(?:affiliat(?:ion|ed)|enrolled|visiting|attendance|academic program)\b',
    'written_agreement':r'\b(?:written agreement|contract|in writing)\b'
}

def flags(text):
    return {k:bool(re.search(v,text,re.I)) for k,v in {**ASSETS,**OPERATIONS,**TRIGGERS}.items()}

def main():
    x=pd.read_csv(ROOT/'input/policy_sentences_cleaned_combined.csv')
    x['sentence_id']=[f'p1r{i:06d}' for i in range(1,len(x)+1)]
    x=x[x.Year.between(1944,2025)].copy()
    f=pd.DataFrame([flags(t) for t in x.Sentence_Cleaned],index=x.index)
    x=pd.concat([x,f],axis=1)
    # Do not require a named asset: pronouns, defined terms, and neighboring
    # clauses are exactly where the original intersection screen loses rules.
    operation_cols=[c for c in OPERATIONS if c not in ['definition_wording','negation_wording']]
    x['expanded_review_candidate']=x[operation_cols].any(axis=1)
    cols=['sentence_id','Institution','Year','File','Sentence_Number','expanded_review_candidate']+list(ASSETS)+list(OPERATIONS)+list(TRIGGERS)
    out=x[cols].copy()
    out['label_origin']='deterministic_regex_review_aid_v2'
    out['legal_classification_status']='not_adjudicated'
    out.to_csv(ROOT/'results/provisional_clause_features.csv',index=False)
    orig=pd.read_csv(ROOT/'results/sentence_index.csv',usecols=['sentence_id','candidate'])
    out=out.merge(orig,on='sentence_id',validate='one_to_one')
    summary={'expanded_review_sentences':int(out.expanded_review_candidate.sum()),'original_candidates':int(out.candidate.sum()),'additional_review_sentences':int((out.expanded_review_candidate & ~out.candidate).sum()),'legal_accuracy_estimated':False}
    (ROOT/'results/extraction_comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(summary)

if __name__=='__main__':main()
