"""Acquire DOI-depositor metadata for human/assistant comparison with primary pages.
HTTP success is not content verification. Ambiguous title searches remain candidates.
"""
import csv
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import requests
import time

ROOT=Path(__file__).resolve().parents[1]
def normalized(s):return re.sub(r'[^a-z0-9]','',s.lower())

def main():
    folder=ROOT/'references/metadata';folder.mkdir(exist_ok=True)
    report=[]
    for row in csv.DictReader((ROOT/'references/search_seeds.tsv').open(),delimiter='\t'):
        p=folder/(row['citekey']+'.json')
        try:
            if p.exists():
                chosen=json.loads(p.read_text())
            else:
                if row['doi']:
                    response=requests.get('https://api.crossref.org/works/'+row['doi'],timeout=45)
                    response.raise_for_status(); chosen=response.json()['message']
                else:
                    response=requests.get('https://api.crossref.org/works',params={'query.bibliographic':row['expected_title'],'rows':5},timeout=45)
                    response.raise_for_status()
                    choices=response.json()['message']['items']
                    chosen=max(choices,key=lambda x:SequenceMatcher(None,normalized(row['expected_title']),normalized(x.get('title',[''])[0])).ratio())
                    (folder/(row['citekey']+'_candidates.json')).write_text(json.dumps([{k:r.get(k) for k in ['DOI','title','author','container-title','published','volume','issue','page']} for r in choices],indent=2))
                # Preserve bibliographic fields, not copyrighted abstracts or reference lists.
                chosen={k:chosen.get(k) for k in ['DOI','title','author','editor','container-title','publisher','published','published-print','published-online','volume','issue','page','article-number','type','ISBN','URL','resource']}
                p.write_text(json.dumps(chosen,indent=2,ensure_ascii=False)+'\n')
                time.sleep(.15)
            title=chosen.get('title',[''])[0]
            score=SequenceMatcher(None,normalized(row['expected_title']),normalized(title)).ratio()
            report.append({'citekey':row['citekey'],'title':title,'DOI':chosen['DOI'],'similarity':score,'status':'metadata_candidate_requires_primary_comparison'})
            print(row['citekey'],chosen['DOI'],round(score,3),title,flush=True)
        except Exception as e:
            report.append({'citekey':row['citekey'],'status':'failed','error':str(e)})
            print(row['citekey'],'FAILED',str(e),flush=True)
    (ROOT/'references/metadata_retrieval_log.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
