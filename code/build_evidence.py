"""Selected AI-assisted readings are not an independent validation standard."""
import json,hashlib
from pathlib import Path
import pandas as pd
from classify_provisions import ASSETS
ROOT=Path(__file__).resolve().parents[1]
def main():
 readings=json.loads((ROOT/'data/illustrative_legal_readings.json').read_text())
 sources={r['source_id']:r for r in json.loads((ROOT/'data/policy_source_snapshot.json').read_text())}
 x=pd.read_csv(ROOT/'results/sentence_index.csv').set_index('sentence_id')
 features=pd.read_csv(ROOT/'results/provisional_clause_features.csv').set_index('sentence_id')
 rows=[]
 for r in readings:
  s=sources[r['source_id']];assert s.get('sha256')
  cached=ROOT/s['local_path']
  if cached.exists():assert hashlib.sha256(cached.read_bytes()).hexdigest()==s['sha256'],'Changed policy source: re-review required'
  for sid in r['sentence_ids']:
   v=x.loc[sid]
   rows.append({k:val for k,val in r.items() if k!='sentence_ids'}|dict(sentence_id=sid,Institution=v.Institution,Year=int(v.Year),File=v.File,Sentence_Number=v.Sentence_Number,corpus_sentence_sha256=v.text_sha256,source_url=s['url'],retrieved_source_sha256=s['sha256'],original_screen_candidate=bool(v.candidate),expanded_review_candidate=bool(features.loc[sid,'expanded_review_candidate']),annotator_type='AI_assisted_close_reading',independent_human_validation=False,enforceability='not_adjudicated'))
 pd.DataFrame(rows).to_csv(ROOT/'results/illustrative_legal_evidence.csv',index=False)
 pd.DataFrame(rows)[['id','sentence_id','original_screen_candidate','expanded_review_candidate','operation','context_status']].to_csv(ROOT/'results/purposive_extraction_error_review.csv',index=False)
 pd.DataFrame([
 dict(institution='Wake Forest University',earlier='1999-labelled corpus / retrieved 2006 reprint',later='2017 Reynolda policy',dimension='Assignment expression',earlier_reading='Institutional ownership presumption',later_reading='Express present assignment in 3.1A',status='illustrative_text_comparison_not_validated_legal_transition',obstacle='Earlier vintage not authenticated; later record mixes campuses; companion copyright policy missing'),
 dict(institution='Wake Forest University',earlier='1999-labelled corpus / retrieved 2006 reprint',later='2017 Reynolda policy',dimension='Student trigger',earlier_reading='Student academic program among alternatives',later_reading='Nonemployee students: supported research/instruction/collaboration/coinventorship',status='direction_indeterminate',obstacle='No common counterfactual student facts, exact earlier vintage or fully matched campus scope'),
 dict(institution='University of Delaware',earlier='1993-labelled corpus',later='2008-labelled corpus',dimension='Observed cleaned text',earlier_reading='Same normalized sentence set',later_reading='Same normalized sentence set',status='lexical_stability_only',obstacle='Archival representation is not operative law')]).to_csv(ROOT/'results/ownership_transition_review.csv',index=False)
 sample=pd.read_csv(ROOT/'results/validation_sample_manifest.csv');f=features.loc[sample.sentence_id]
 pd.DataFrame([dict(category=c,sample_flagged_sentences=int(f[c].sum()),reference_standard_labels=0) for c in ASSETS]).to_csv(ROOT/'results/validation_category_coverage.csv',index=False)
 report=dict(probability_sample_sentences=len(sample),sample_institutions=sample.Institution.nunique(),purposive_readings=len(readings),purposive_sentence_links=len(rows),independent_human_annotators=0,reference_standard_labels=0,precision=None,recall=None,agreement=None,reason='No independent reference standard; purposive AI-assisted readings diagnose errors without estimating accuracy.')
 (ROOT/'results/validation_status.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
if __name__=='__main__':main()
