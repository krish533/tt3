"""Optional live recovery; archived bytes are local, metadata is shareable.

Never equate a successful HTTP response with historical provenance validation.
"""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone
import requests

ROOT=Path(__file__).resolve().parents[1]

def main():
    cache=ROOT/'input/policies';cache.mkdir(parents=True,exist_ok=True)
    logs=[]
    for r in csv.DictReader((ROOT/'data/policy_sources.csv').open()):
        item=dict(r)
        item['retrieved_at_utc']=datetime.now(timezone.utc).isoformat()
        try:
            response=requests.get(r['url'],timeout=45)
            item.update(http_status=response.status_code,resolved_url=response.url)
            response.raise_for_status()
            extension='.pdf' if response.content.startswith(b'%PDF') else '.html'
            p=cache/(r['source_id']+extension);p.write_bytes(response.content)
            item.update(sha256=hashlib.sha256(response.content).hexdigest(),bytes=len(response.content),local_path=str(p.relative_to(ROOT)),format=extension[1:])
            if extension=='.pdf':
                subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
            else:
                from html.parser import HTMLParser
                class Extract(HTMLParser):
                    def __init__(self):super().__init__();self.parts=[]
                    def handle_data(self,data):self.parts.append(data)
                parser=Extract();parser.feed(response.text)
                p.with_suffix('.txt').write_text('\n'.join(parser.parts))
            item['retrieval_status']='retrieved_not_yet_matched'
        except Exception as e:
            item.update(retrieval_status='failed',error=str(e))
        logs.append(item)
        print(r['source_id'],item['retrieval_status'])
    (ROOT/'results/policy_retrieval_log.json').write_text(json.dumps(logs,indent=2)+'\n')

if __name__=='__main__':main()
