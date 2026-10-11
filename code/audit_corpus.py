"""Freeze the supplied population without repairing or silently dropping rows."""
import hashlib
import json
from pathlib import Path
import re
import numpy as np
import pandas as pd
from extract_ownership import CATEGORIES, RULES

ROOT = Path(__file__).resolve().parents[1]
KEY = ['Institution', 'Year', 'File']
SEED = 2031

def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def normalize(text):
    return ' '.join(str(text).casefold().split())

def audit(source, panel, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(source, low_memory=False)
    raw['source_row'] = np.arange(1, len(raw) + 1)
    raw['sentence_id'] = raw.source_row.map(lambda n: f'p1r{n:06d}')
    years = pd.to_numeric(raw.Year, errors='coerce')
    included = years.between(1944, 2025) & raw.Sentence_Cleaned.notna()
    excluded = raw.loc[~included, ['sentence_id'] + KEY + ['Sentence_Number']].copy()
    excluded['reason'] = 'outside_1944_2025_or_missing_text'
    excluded.to_csv(out / 'exclusions.csv', index=False)
    x = raw.loc[included].copy()
    for key, pattern in {**CATEGORIES, **RULES}.items():
        x[key] = x.Sentence_Cleaned.str.contains(pattern, flags=re.I, regex=True)
    x['candidate'] = x[list(CATEGORIES)].any(axis=1) & x[list(RULES)].any(axis=1)
    x['text_sha256'] = x.Sentence_Cleaned.map(digest)
    x['normalized_sha256'] = x.Sentence_Cleaned.map(normalize).map(digest)
    x['sentence_key_collision'] = x.duplicated(KEY + ['Sentence_Number'], keep=False)
    x['document_id'] = x[KEY].astype(str).agg('|'.join, axis=1).map(digest).str[:20]
    x['decade'] = x.Year // 10 * 10
    x[['sentence_id','source_row','document_id'] + KEY + ['Sentence_Number','text_sha256','normalized_sha256','sentence_key_collision','candidate']].to_csv(out / 'sentence_index.csv', index=False)
    x.loc[x.sentence_key_collision, ['sentence_id'] + KEY + ['Sentence_Number','text_sha256']].to_csv(out / 'sentence_identifier_collisions.csv', index=False)
    documents=[]
    for (inst, year, file), g in x.groupby(KEY, sort=True):
        ordered = g.sort_values(['Sentence_Number','source_row'], kind='stable')
        texts = ordered.Sentence_Cleaned.map(normalize)
        numbers = pd.to_numeric(g.Sentence_Number)
        file_years = re.findall(r'(?:19|20)\d{2}', file)
        documents.append(dict(document_id=g.document_id.iloc[0], Institution=inst, Year=int(year), File=file,
            sentences=len(g), candidates=int(g.candidate.sum()),
            sentence_key_collision_rows=int(g.sentence_key_collision.sum()),
            duplicate_normalized_text_rows=int(texts.duplicated().sum()),
            missing_integer_sentence_numbers=int(numbers.max()-numbers.min()+1-numbers.nunique()),
            filename_year_mismatch=bool(file_years and str(year) not in file_years),
            text_sha256=digest('\n'.join(texts)),
            context_status='context_unverified', vintage_status='upstream_label_unverified'))
    docs=pd.DataFrame(documents)
    docs['same_text_document_groups']=docs.groupby('text_sha256').text_sha256.transform('size')
    docs.to_csv(out / 'document_provenance.csv',index=False)
    docs[docs.same_text_document_groups.gt(1)].to_csv(out / 'identical_document_text.csv',index=False)
    insts=x.groupby('Institution').agg(first_year=('Year','min'),last_year=('Year','max'),observed_years=('Year','nunique'),sentences=('Year','size')).reset_index()
    insts['trimmed_identifier']=insts.Institution.str.strip()
    insts['whitespace_issue']=insts.Institution.ne(insts.trimmed_identifier)
    insts['normalized_identifier']=insts.Institution.map(normalize)
    insts['normalization_collision']=insts.normalized_identifier.duplicated(keep=False)
    insts.to_csv(out / 'institution_identifier_audit.csv',index=False)
    years_table=x.groupby(['Institution','Year']).agg(sentences=('sentence_id','size'),candidates=('candidate','sum'),source_files=('File','nunique')).reset_index()
    years_table.to_csv(out / 'frozen_observed_population.csv',index=False)
    # Only identifier columns from Paper 1's panel enter this audit.
    p=pd.read_csv(panel, usecols=['Institution','Year','Source_Year','Is_Carried_Forward'])
    p=p[p.Year.between(1944,2025)]
    observed=p[p.Is_Carried_Forward.eq(0)]
    assert set(map(tuple, observed[['Institution','Year']].values)) == set(map(tuple,years_table[['Institution','Year']].values))
    assert (len(x),len(years_table),x.Institution.nunique(),len(p),len(docs),int(x.candidate.sum())) == (87159,480,150,4277,518,2779)
    transitions=[]
    for inst, group in years_table.groupby('Institution'):
        rows=group.sort_values('Year').to_dict('records')
        for a,b in zip(rows,rows[1:]):
            ga=x[(x.Institution==inst)&(x.Year==a['Year'])]
            gb=x[(x.Institution==inst)&(x.Year==b['Year'])]
            sa=set(ga.normalized_sha256);sb=set(gb.normalized_sha256)
            transitions.append(dict(Institution=inst,from_year=a['Year'],to_year=b['Year'],gap=b['Year']-a['Year'],
                from_source_files=a['source_files'],to_source_files=b['source_files'],
                sentence_jaccard=len(sa&sb)/len(sa|sb),same_sentence_set=sa==sb,
                source_bundle_changed=a['source_files']!=b['source_files'],
                candidate_change=b['candidates']-a['candidates'],
                legal_transition_status='not_adjudicated'))
    t=pd.DataFrame(transitions)
    t.to_csv(out / 'observed_vintage_pairs.csv',index=False)
    # Sampling is reproducible and has known inclusion probabilities; it is NOT validation.
    sampled=[]
    for (decade, candidate), g in x.groupby(['decade','candidate'],sort=True):
        selected=g.sample(n=min(12,len(g)), random_state=SEED).copy()
        selected['stratum_population']=len(g)
        selected['stratum_sample']=len(selected)
        selected['inclusion_probability']=len(selected)/len(g)
        sampled.append(selected)
    s=pd.concat(sampled).sort_values('source_row')
    samplecols=['sentence_id','document_id']+KEY+['Sentence_Number','decade','candidate','stratum_population','stratum_sample','inclusion_probability']
    s[samplecols].to_csv(out/'validation_sample_manifest.csv',index=False)
    s[samplecols+['Sentence_Cleaned']].to_csv(out/'validation_sample_text.csv',index=False)
    annotation=s[['sentence_id']].copy()
    for col in ['annotator_id','annotator_type','source_verified','operative','rights_holder','legal_operation','knowledge_category','trigger','qualifications','confidence','notes']:
        annotation[col]=''
    annotation.to_csv(out/'validation_annotation_template.csv',index=False)
    # Local reconstructed context preserves all rows and discloses collisions.
    context=out/'context';context.mkdir(exist_ok=True)
    for docid,g in x.groupby('document_id'):
        g=g.sort_values(['Sentence_Number','source_row'],kind='stable')
        heading=f"{g.Institution.iloc[0]} | {g.Year.iloc[0]} | {g.File.iloc[0]}\nRECONSTRUCTED CLEANED SENTENCES; NOT ORIGINAL PARAGRAPHS OR SOURCE VERIFICATION\n"
        (context/f'{docid}.txt').write_text(heading+'\n'.join(f'[{r.sentence_id}; sentence {r.Sentence_Number}] {r.Sentence_Cleaned}' for r in g.itertuples()))
    summary=dict(raw_rows=len(raw),included_rows=len(x),excluded_rows=len(excluded),institutions=x.Institution.nunique(),observed_records=len(years_table),document_keys=len(docs),unique_filenames=x.File.nunique(),panel_rows=len(p),carried_forward_rows=int(p.Is_Carried_Forward.sum()),candidate_sentences=int(x.candidate.sum()),candidate_records=int(years_table.candidates.gt(0).sum()),duplicate_raw_rows=int(raw.drop(columns=['source_row','sentence_id']).duplicated().sum()),duplicate_sentence_keys=int(x.duplicated(KEY+['Sentence_Number']).sum()),collision_rows=int(x.sentence_key_collision.sum()),duplicate_normalized_sentences_within_document=int(docs.duplicate_normalized_text_rows.sum()),identical_text_document_groups=int(docs.same_text_document_groups.gt(1).sum()),multi_file_records=int(years_table.source_files.gt(1).sum()),within_institution_pairs=len(t),institutions_with_pairs=t.Institution.nunique(),identical_sentence_set_pairs=int(t.same_sentence_set.sum()),bundle_size_changed_pairs=int(t.source_bundle_changed.sum()),filename_year_mismatches=int(docs.filename_year_mismatch.sum()),validation_sample_size=len(s),validation_completed=False,minimum_sentence_characters=int(x.Sentence_Cleaned.str.len().min()),missing_values=raw.isna().sum().to_dict())
    (out/'corpus_audit.json').write_text(json.dumps(summary,indent=2,default=int)+'\n')
    screen=dict(institution_year_groups=len(years_table),institutions=int(x.Institution.nunique()),earliest_year=int(x.Year.min()),latest_year=int(x.Year.max()),candidate_sentences=int(x.candidate.sum()),candidate_groups=int(years_table.candidates.gt(0).sum()))
    (out/'screening_summary.json').write_text(json.dumps(screen,indent=2)+'\n')
    (out/'source_sha256.txt').write_text(hashlib.sha256(Path(source).read_bytes()).hexdigest()+'  input/policy_sentences_cleaned_combined.csv\n')
    print(json.dumps(summary,indent=2,default=int))
    return x,docs,t

if __name__=='__main__':
    audit(ROOT/'input/policy_sentences_cleaned_combined.csv',ROOT/'input/policy_level_indices_institution_year.csv',ROOT/'results')
