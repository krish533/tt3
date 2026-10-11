"""Observed-vintage lexical diagnostics; never estimates legal expansion.

All uncertainty intervals concern archive-conditioned lexical quantities, not
national sampling uncertainty, source authenticity, or legal interpretation.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from classify_provisions import ASSETS

ROOT=Path(__file__).resolve().parents[1]
SEED=2031

def main():
    x=pd.read_csv(ROOT/'results/provisional_clause_features.csv')
    assets=list(ASSETS)
    v=x.groupby(['Institution','Year'])[assets].max().reset_index()
    v['named_categories']=v[assets].sum(axis=1)
    v.to_csv(ROOT/'results/observed_category_mentions.csv',index=False)
    pairs=[]
    for inst,g in v.groupby('Institution'):
        rows=g.sort_values('Year').to_dict('records')
        for a,b in zip(rows,rows[1:]):
            for c in assets:
                pairs.append(dict(Institution=inst,from_year=a['Year'],to_year=b['Year'],category=c,before=int(a[c]),after=int(b[c]),change=int(b[c])-int(a[c])))
    pairs=pd.DataFrame(pairs)
    pairs.to_csv(ROOT/'results/category_mention_pairs.csv',index=False)
    table=pairs.groupby(['category','before','after']).size().unstack(['before','after'],fill_value=0).reindex(columns=pd.MultiIndex.from_product([[0,1],[0,1]]),fill_value=0)
    table.columns=['absent_absent','absent_present','present_absent','present_present']
    table.reset_index().to_csv(ROOT/'results/lexical_transition_matrix.csv',index=False)
    weighted=[]
    for cat,g in pairs.groupby('category'):
        means=g.groupby('Institution').change.mean().to_numpy()
        rng=np.random.default_rng(SEED)
        boot=rng.choice(means,size=(5000,len(means)),replace=True).mean(axis=1)
        lo,hi=np.quantile(boot,[.025,.975])
        weighted.append(dict(category=cat,universities=len(means),pairs=len(g),pair_weighted_mean=g.change.mean(),institution_weighted_mean=means.mean(),bootstrap_low=lo,bootstrap_high=hi))
    pd.DataFrame(weighted).to_csv(ROOT/'results/lexical_institution_weighted_changes.csv',index=False)
    # Scope comparability diagnostics; unchanged file count does not certify scope.
    links=pd.read_csv(ROOT/'results/observed_vintage_pairs.csv')
    comparison=pairs.merge(links[['Institution','from_year','to_year','source_bundle_changed','gap']],on=['Institution','from_year','to_year'],validate='many_to_one')
    sensitivity=[]
    for name,frame in [('all_pairs',comparison),('unchanged_file_count',comparison[~comparison.source_bundle_changed]),('both_endpoints_1980_onward',comparison[comparison.from_year.ge(1980)]),('gap_at_most_10_years',comparison[comparison.gap.le(10)])]:
        for cat,g in frame.groupby('category'):
            sensitivity.append(dict(sample=name,category=cat,pairs=len(g),universities=g.Institution.nunique(),appearances=int(((g.before==0)&(g.after==1)).sum()),disappearances=int(((g.before==1)&(g.after==0)).sum()),pair_mean=g.change.mean(),university_mean=g.groupby('Institution').change.mean().mean()))
    pd.DataFrame(sensitivity).to_csv(ROOT/'results/lexical_pair_sensitivity.csv',index=False)
    corpus=pd.read_csv(ROOT/'input/policy_sentences_cleaned_combined.csv')
    corpus=corpus[corpus.Year.between(1944,2025)].copy()
    from extract_ownership import CATEGORIES,RULES
    import re
    def counts(frame,name):
        a=frame.Sentence_Cleaned.str.contains('|'.join(CATEGORIES.values()),flags=re.I,regex=True)
        r=frame.Sentence_Cleaned.str.contains('|'.join(RULES.values()),flags=re.I,regex=True)
        return dict(sensitivity=name,sentences=len(frame),candidates=int((a&r).sum()),per_1000=float(1000*(a&r).mean()),observed_records=len(frame[['Institution','Year']].drop_duplicates()),institutions=frame.Institution.nunique())
    corpus['norm']=corpus.Sentence_Cleaned.str.casefold().str.split().str.join(' ')
    checks=[counts(corpus,'primary_unchanged'),counts(corpus.drop_duplicates(['Institution','Year','File','norm']),'deduplicate_normalized_sentences_within_file'),counts(corpus[~corpus.Institution.eq('Georgia Institute of Technology')],'exclude_sentence_identifier_collision_institution'),counts(corpus[corpus.Year.ge(1980)],'observed_1980_onward')]
    pd.DataFrame(checks).to_csv(ROOT/'results/screening_sensitivity.csv',index=False)
    decades=corpus.assign(decade=corpus.Year//10*10).groupby('decade').agg(sentences=('Year','size'),institutions=('Institution','nunique'))
    fig,ax=plt.subplots(figsize=(7,3.5))
    years=np.arange(1940,2030,10)
    obs=corpus[['Institution','Year']].drop_duplicates().assign(decade=lambda f:f.Year//10*10).groupby('decade').size().reindex(years,fill_value=0)
    ax.bar(years,obs,width=7,color='0.35')
    ax.set(xlabel='Decade of upstream vintage label',ylabel='Directly observed institution-years',xticks=years)
    ax.spines[['top','right']].set_visible(False)
    fig.tight_layout()
    (ROOT/'manuscript/figures').mkdir(exist_ok=True)
    fig.savefig(ROOT/'manuscript/figures/archival_coverage.pdf',metadata={'CreationDate':None,'ModDate':None})
    fig.savefig(ROOT/'manuscript/figures/archival_coverage.png',dpi=180)
    plt.close(fig)
    # No point estimates are manufactured for unadjudicated legal outcomes.
    pd.DataFrame([{'outcome':c,'eligible_observed_records':480,'fully_adjudicated_records':0,'lower_bound':0.0,'upper_bound':1.0,'status':'unidentified_without_contextual_reference_standard'} for c in ['institutional_ownership','assignment_obligation','creator_exception','student_exception']]).to_csv(ROOT/'results/legal_identification_bounds.csv',index=False)
    print(pd.DataFrame(checks).to_string(index=False))

if __name__=='__main__':main()
