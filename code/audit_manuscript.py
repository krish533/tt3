"""Citation resolution, numerical claim map and render-independent checks."""
import json,re
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
 text=(ROOT/'manuscript/main.tex').read_text()
 refs=json.loads((ROOT/'references/accepted_records.json').read_text());keys={r['key'] for r in refs}
 used=set()
 for group in re.findall(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}',text):used.update(group.split(','))
 assert not used-keys,used-keys
 assert not keys-used,keys-used
 abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',text,re.S)[1]
 words=re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",abstract)
 assert len(words)<=150,len(words)
 for flag in ['PLACEHOLDER','TODO','[citation needed]']:assert flag not in text
 assert text.count('\\begin{table}')==6 and text.count('\\begin{figure}')==1
 report=dict(bibliography_entries=len(keys),cited_entries=len(used),unresolved_citations=[],uncited_entries=[],abstract_words=len(words),tables=6,figures=1,legal_population_accuracy_estimated=False,submission_ready=False)
 (ROOT/'results/manuscript_audit.json').write_text(json.dumps(report,indent=2)+'\n')
 claims=[
 ('Population and screening numbers','results/corpus_audit.json','macros in manuscript/numbers.tex; Tables 1–2','generated'),
 ('2,703 within-document duplicates; 15 participating groups','results/corpus_audit.json','duplicate_normalized_sentences_within_document; identical_text_document_groups','checked'),
 ('35 bundle-size changes','results/observed_vintage_pairs.csv','source_bundle_changed sum','checked'),
 ('57/24 data and 48/27 software lexical transitions','results/lexical_transition_matrix.csv','absent_present and present_absent','checked'),
 ('129 university means; 5,000 bootstrap draws; 95% intervals','code/analyze_history.py','SEED=2031; size=(5000,len(means)); quantiles .025,.975','checked'),
 ('Gap and file-count sensitivity','results/lexical_pair_sensitivity.csv','233 short-gap pairs; 97 universities; generated ShortSoftware and ShortData macros','generated'),
 ('178 validation sentences; 68 institutions','results/validation_status.json','probability_sample_sentences; sample_institutions','checked'),
 ('Zero fully adjudicated records; bounds [0,1]','results/legal_identification_bounds.csv','fully_adjudicated_records; lower_bound; upper_bound','checked'),
 ('Selected legal readings','results/illustrative_legal_evidence.csv','sentence IDs, original source section and hashes','AI-assisted; independent review pending'),
 ('Dates in laws and scholarship','references/reference_audit.csv','primary links and correction log','individually logged; access limits retained')]
 pd.DataFrame(claims,columns=['claim','source','locator','status']).to_csv(ROOT/'results/manuscript_claim_audit.csv',index=False)
 print(report)
if __name__=='__main__':main()
