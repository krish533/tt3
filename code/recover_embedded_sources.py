"""Inventory source-embedded URLs; optionally retrieve plausible policy links.
A referenced link is NOT automatically the source of the enclosing policy.
Downloads remain local. No legal labels or vintage authentication follow from HTTP 200.
"""
import argparse,concurrent.futures,hashlib,json,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
import pandas as pd
import requests
ROOT=Path(__file__).resolve().parents[1]
def inventory():
 x=pd.read_csv(ROOT/'input/policy_sentences_cleaned_combined.csv');rows=[]
 for i,r in x.iterrows():
  if not 1944<=r.Year<=2025:continue
  for raw in re.findall(r'https?://[^\s<>\"]+',str(r.Sentence_Cleaned)):
   u=raw.rstrip('.,);]');host=urlsplit(u).hostname or ''
   candidate=host.endswith('.edu') and bool(re.search(r'policy|policies|patent|intell|copyright|handbook|manual|7-002',u,re.I))
   rows.append(dict(sentence_id=f'p1r{i+1:06d}',Institution=r.Institution,Year=int(r.Year),File=r.File,raw_url=raw,cleaned_url=u,retrieval_candidate=candidate,relationship='embedded_reference_not_verified_source'))
 out=pd.DataFrame(rows);out.to_csv(ROOT/'results/embedded_url_inventory.csv',index=False);return out

def fetch(u):
 p=urlsplit(u);url=urlunsplit(('https',p.netloc,p.path,p.query,''))
 item=dict(embedded_url=u,attempted_url=url,retrieved_at_utc=datetime.now(timezone.utc).isoformat(),context_status='not_matched_not_vintage_verified')
 try:
  response=requests.get(url,timeout=(8,18),stream=True);item.update(http_status=response.status_code,resolved_url=response.url);response.raise_for_status()
  data=bytearray()
  for chunk in response.iter_content(65536):
   data.extend(chunk)
   if len(data)>25_000_000:raise ValueError('25 MB retrieval limit')
  digest=hashlib.sha256(data).hexdigest();fmt='pdf' if data[:4]==b'%PDF' else 'html'
  target=ROOT/'input/embedded_sources'/f'{digest}.{fmt}';target.parent.mkdir(exist_ok=True);target.write_bytes(data)
  if fmt=='pdf':
   subprocess.run(['pdftotext','-layout',str(target),str(target.with_suffix('.txt'))],capture_output=True,timeout=30)
  item.update(status='downloaded_unreviewed',sha256=digest,bytes=len(data),format=fmt,local_path=str(target.relative_to(ROOT)))
 except Exception as e:item.update(status='failed',error=str(e))
 return item

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fetch',action='store_true');a=ap.parse_args();x=inventory();urls=sorted(set(x.loc[x.retrieval_candidate,'cleaned_url']))
 print('Embedded URL occurrences',len(x),'unique',x.cleaned_url.nunique(),'policy-link candidates',len(urls),flush=True)
 if a.fetch:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   rows=list(pool.map(fetch,urls))
  (ROOT/'results/embedded_source_retrieval_log.json').write_text(json.dumps(rows,indent=2)+'\n')
  print(pd.Series([r['status'] for r in rows]).value_counts().to_dict())
if __name__=='__main__':main()
