"""Numerical LaTeX inputs; all table values come from released outputs."""
import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
LABEL={'patentable_inventions':'Inventions/patents','research_datasets':'Research data/databases','scholarly_publications':'Scholarly/publication terms','teaching_materials':'Teaching materials','tangible_research_property':'Tangible research property','biological_materials':'Biological materials','emerging_technologies':'AI/mask-work/semiconductor terms','software':'Software','algorithms':'Algorithms'}
def table(name,header,rows,spec):
 p=ROOT/'manuscript/tables';p.mkdir(exist_ok=True)
 (p/(name+'.tex')).write_text('\\begin{tabular}{'+spec+'}\n\\toprule\n'+' & '.join(header)+r' \\'+'\n\\midrule\n'+'\n'.join(' & '.join(map(str,row))+r' \\' for row in rows)+'\n\\bottomrule\n\\end{tabular}\n')
def prose_table(name,header,rows):
 spec=r'@{}>{\raggedright\arraybackslash}p{.23\linewidth}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X@{}'
 (ROOT/'manuscript/tables'/f'{name}.tex').write_text('\\begin{tabularx}{\\linewidth}{'+spec+'}\n\\toprule\n'+' & '.join(header)+r' \\'+'\n\\midrule\n'+'\n'.join(' & '.join(str(c).replace('&',r'\&').replace('_',r'\_') for c in row)+r' \\' for row in rows)+'\n\\bottomrule\n\\end{tabularx}\n')
def main():
 a=json.loads((ROOT/'results/corpus_audit.json').read_text())
 macros={'Universities':a['institutions'],'Observed':a['observed_records'],'Sentences':a['included_rows'],'Candidates':a['candidate_sentences'],'CandidateRecords':a['candidate_records'],'DocKeys':a['document_keys'],'Panel':a['panel_rows'],'Carried':a['carried_forward_rows'],'Pairs':a['within_institution_pairs'],'PairUniversities':a['institutions_with_pairs'],'ValidationN':a['validation_sample_size'],'CollisionRows':a['collision_rows'],'MultiFiles':a['multi_file_records'],'BundleChanged':a['bundle_size_changed_pairs']}
 sensitivity=pd.read_csv(ROOT/'results/lexical_pair_sensitivity.csv').set_index(['sample','category'])
 short=sensitivity.loc[('gap_at_most_10_years','software')]
 macros.update(ShortPairs=int(short.pairs),ShortUniversities=int(short.universities),ShortSoftware=f'{short.university_mean:.3f}',ShortData=f"{sensitivity.loc[('gap_at_most_10_years','research_datasets'),'university_mean']:.3f}")
 (ROOT/'manuscript/numbers.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+(format(v,',') if isinstance(v,int) else str(v))+'}' for k,v in macros.items())+'\n')
 table('population',['Quantity','Count'],[['Universities',a['institutions']],['Observed institution-years',a['observed_records']],['Institution-year-filename groups',a['document_keys']],['Included cleaned sentences',format(a['included_rows'],',')],['Panel rows (not documents)',format(a['panel_rows'],',')],['Carried-forward rows',format(a['carried_forward_rows'],',')],['Original-screen sentences',format(a['candidate_sentences'],',')],['Records with screen matches',a['candidate_records']],['Adjacent observed pairs',a['within_institution_pairs']],['Universities with pairs',a['institutions_with_pairs']]],'lr')
 d=pd.read_csv(ROOT/'results/screening_by_decade.csv')
 table('decades',['Decade','Records','Universities','Sentences','Matches','Per 1,000'],[[int(r.decade),int(r.documents),int(r.institutions),format(int(r.sentences),','),int(r.candidates),f'{r.per_1000_sentences:.1f}'] for r in d.itertuples()],'lrrrrr')
 t=pd.read_csv(ROOT/'results/lexical_transition_matrix.csv')
 table('transitions',['Category','0 to 0','0 to 1','1 to 0','1 to 1'],[[LABEL[r.category],r.absent_absent,r.absent_present,r.present_absent,r.present_present] for r in t.itertuples()],'lrrrr')
 w=pd.read_csv(ROOT/'results/lexical_institution_weighted_changes.csv')
 table('weighted',['Category','Pair mean','University mean','Bootstrap interval'],[[LABEL[r.category],f'{r.pair_weighted_mean:.3f}',f'{r.institution_weighted_mean:.3f}',f'[{r.bootstrap_low:.3f}, {r.bootstrap_high:.3f}]'] for r in w.itertuples()],'lrrl')
 s=pd.read_csv(ROOT/'results/screening_sensitivity.csv');labels=['Primary unchanged','Deduplicate within file','Exclude Georgia Tech','Observed 1980 onward']
 table('sensitivity',['Population','Sentences','Matches','Per 1,000'],[[label,format(r.sentences,','),format(r.candidates,','),f'{r.per_1000:.2f}'] for label,r in zip(labels,s.itertuples())],'lrrr')
 rel=pd.read_csv(ROOT/'results/substantive_relationship_changes.csv').set_index('id')
 selected=['UT01','UT02','UT05','HI01','HI02','HI03','HI06']
 prose_table('substantive_rules',['Relationship','Earlier endpoint','Later endpoint'],[[('Utah: ' if key.startswith('UT') else "Hawai\'i: ")+rel.loc[key,'dimension'],rel.loc[key,'before'],rel.loc[key,'after']] for key in selected])
 pairs=pd.read_csv(ROOT/'results/substantive_pair_classification.csv')
 prose_table('definition_rights',['Comparison','Definition or enumeration','Allocation conclusion'],[
 ['Utah, 1999--2013',pairs.iloc[0].definition_change,'Present assignment and revised conditions coexist with a narrower resource branch. Mixed; net expansion indeterminate.'],
 ["Hawai\'i, 1985--2020",pairs.iloc[1].definition_change,'Qualified creator baseline persists; use and exception terms change. Earlier faculty contract limits claims of newly created rights.']])
 audit=[dict(item='Table 1',file='manuscript/tables/population.tex',source='results/corpus_audit.json',meaning='Corpus accounting'),dict(item='Table 2',file='manuscript/tables/substantive_rules.tex',source='results/substantive_relationship_changes.csv',meaning='Seven selected dimensions from two comparisons; not independent revisions'),dict(item='Table 3',file='manuscript/tables/definition_rights.tex',source='results/substantive_pair_classification.csv',meaning='Case-level naming and allocation; no population frequencies'),dict(item='Table 4',file='manuscript/tables/transitions.tex',source='results/lexical_transition_matrix.csv',meaning='Category mentions, not rules'),dict(item='Figure 1',file='manuscript/figures/archival_coverage.pdf',source='results/frozen_observed_population.csv',meaning='Observed vintage counts')]
 pd.DataFrame(audit).to_csv(ROOT/'results/table_figure_audit.csv',index=False)
if __name__=='__main__':main()
