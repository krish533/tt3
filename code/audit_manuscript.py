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
 assert text.count('\\begin{table}')==4 and text.count('\\begin{figure}')==1
 report=dict(bibliography_entries=len(keys),cited_entries=len(used),unresolved_citations=[],uncited_entries=[],abstract_words=len(words),tables=4,figures=1,legal_population_accuracy_estimated=False,submission_ready=False)
 (ROOT/'results/manuscript_audit.json').write_text(json.dumps(report,indent=2)+'\n')
 claims=[
 ('Population and screening numbers','results/corpus_audit.json','macros in manuscript/numbers.tex; Table 1','generated'),
 ('2,703 within-document duplicates; 15 participating groups','results/corpus_audit.json','duplicate_normalized_sentences_within_document; identical_text_document_groups','checked'),
 ('35 bundle-size changes','results/observed_vintage_pairs.csv','source_bundle_changed sum','checked'),
 ('57/24 data and 48/27 software lexical transitions','results/lexical_transition_matrix.csv','absent_present and present_absent','checked'),
 ('129 university means; 5,000 bootstrap draws; 95% intervals','code/analyze_history.py','SEED=2031; size=(5000,len(means)); quantiles .025,.975','checked'),
 ('Gap and file-count sensitivity','results/lexical_pair_sensitivity.csv','233 short-gap pairs; 97 universities; generated ShortSoftware and ShortData macros','generated'),
 ('178 validation sentences; 68 institutions','results/validation_status.json','probability_sample_sentences; sample_institutions','checked'),
 ('Two institutions; 13 relationships; one adjacent and one nonadjacent comparison; 329 adjacent pairs unclassified','results/substantive_analysis_summary.json','selected_institutions; relationship_comparisons; selected_adjacent_comparisons; additional_nonadjacent_endpoint_comparisons; unreviewed_adjacent_pairs','generated'),
 ('Tables 2–3 substantive comparisons','results/substantive_relationship_changes.csv; results/substantive_pair_classification.csv','before/after source sections, corpus IDs, source hashes, qualifications','AI-assisted; independent human review pending'),
 ('Selected legal readings','results/illustrative_legal_evidence.csv','sentence IDs, original source section and hashes','AI-assisted; independent review pending'),
 ('Dates in laws and scholarship','references/reference_audit.csv','primary links and correction log','individually logged; access limits retained')]
 pd.DataFrame(claims,columns=['claim','source','locator','status']).to_csv(ROOT/'results/manuscript_claim_audit.csv',index=False)
 print(report)
if __name__=='__main__':main()
