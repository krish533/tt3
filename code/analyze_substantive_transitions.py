"""Rebuild source-linked, explicitly curated legal comparisons.

Semantic codes are disclosed research inputs, not predictions or ground truth.
Tests check traceability and denominators, not legal correctness.
"""
import csv, hashlib, json, re
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
def norm(s): return re.sub(r'[^a-z0-9]+','',str(s).lower())
def main():
    spec=json.loads((ROOT/'data/substantive_comparisons.json').read_text())
    sources={r['source_id']:r for r in json.loads((ROOT/'data/revision_source_snapshot.json').read_text())}
    for r in sources.values():
        path=ROOT/r['local_path']
        if path.exists(): assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256'],r['source_id']
    corpus=pd.read_csv(ROOT/'input/policy_sentences_cleaned_combined.csv')
    pairs={p['pair_id']:p for p in spec['pairs']}
    base=pd.read_csv(ROOT/'results/observed_vintage_pairs.csv')
    pop=set(map(tuple,pd.read_csv(ROOT/'results/frozen_observed_population.csv')[['Institution','Year']].values))
    rows=[]; links=[]; local=[]
    for r in spec['relationships']:
        p=pairs[r['pair_id']]; out={**r,'institution':p['institution'],'from_year':p['from_year'],'to_year':p['to_year'],
          'coding_status':spec['coding_status'],'independent_human_validation':False,'enforceability':'not_adjudicated',
          'comparison_scope':p['scope'],'source_authentication':p['authentication']}
        for end,year in [('before','from_year'),('after','to_year')]:
            ids=r[end+'_ids']; snippets=[]
            for i in ids:
                item=corpus.iloc[i-1]
                assert item.Institution==p['institution'] and int(item.Year)==p[year],(r['id'],i)
                snippets.append(item.Sentence_Cleaned)
                links.append(dict(relationship_id=r['id'],pair_id=p['pair_id'],endpoint=end,sentence_id=f'p1r{i:06d}',
                    Institution=item.Institution,Year=int(item.Year),File=item.File,
                    text_sha256=hashlib.sha256(item.Sentence_Cleaned.encode()).hexdigest()))
                local.append(dict(relationship_id=r['id'],endpoint=end,sentence_id=f'p1r{i:06d}',text=item.Sentence_Cleaned))
            assert norm(r[end+'_quote']) in norm(' '.join(snippets)),(r['id'],end,r[end+'_quote'])
            src=sources[p['earlier_source' if end=='before' else 'later_source']]
            out[end+'_source_url']=src['url']; out[end+'_source_sha256']=src['sha256']
            out[end+'_ids']=';'.join(f'p1r{i:06d}' for i in ids)
        out['context_sources']=';'.join(p['context_sources'])
        rows.append(out)
    for p in pairs.values():
        assert (p['institution'],p['from_year']) in pop and (p['institution'],p['to_year']) in pop
        match=base.Institution.eq(p['institution']) & base.from_year.eq(p['from_year']) & base.to_year.eq(p['to_year'])
        assert bool(match.any())==p['adjacent_in_frozen_corpus']
    pd.DataFrame(rows).to_csv(ROOT/'results/substantive_relationship_changes.csv',index=False)
    pd.DataFrame(links).to_csv(ROOT/'results/substantive_evidence_links.csv',index=False)
    pd.DataFrame(local).to_csv(ROOT/'input/substantive_context_review.csv',index=False)
    pd.DataFrame(spec['pairs']).to_csv(ROOT/'results/substantive_pair_classification.csv',index=False)
    base['substantive_review_status']='not_contextually_classified'
    base['substantive_pair_id']=''
    for p in pairs.values():
        if p['adjacent_in_frozen_corpus']:
            mask=base.Institution.eq(p['institution']) & base.from_year.eq(p['from_year']) & base.to_year.eq(p['to_year'])
            base.loc[mask,'substantive_review_status']='selected_relationships_AI_checked; whole_pair_not_adjudicated'
            base.loc[mask,'substantive_pair_id']=p['pair_id']
    base.to_csv(ROOT/'results/substantive_comparability_register.csv',index=False)
    summary=dict(frozen_adjacent_pairs=len(base),selected_adjacent_comparisons=sum(p['adjacent_in_frozen_corpus'] for p in pairs.values()),
       additional_nonadjacent_endpoint_comparisons=sum(not p['adjacent_in_frozen_corpus'] for p in pairs.values()),
       selected_institutions=len({p['institution'] for p in pairs.values()}),relationship_comparisons=len(rows),
       unreviewed_adjacent_pairs=int(base.substantive_pair_id.eq('').sum()),fully_adjudicated_pairs=0,
       independently_validated_pairs=0,population_transition_frequencies_estimated=False,
       note='Do not count relationship rows as independent policy revisions. Mixed outcomes cannot be collapsed into a scalar expansion score.')
    (ROOT/'results/substantive_analysis_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(summary)

if __name__=='__main__': main()
