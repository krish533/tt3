"""Optional, TLS-verified retrieval of official historical comparison sources.

Raw documents stay in ignored input/. Metadata and hashes are retained.
DOCX extraction is research text extraction, not a Word submission export.
"""
import hashlib, json, subprocess, zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
import requests

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'utah_history': 'https://regulations.utah.edu/research/revisions_7/7-002R4-background.docx',
    'utah_r3': 'https://regulations.utah.edu/_resources/documents/ppm-archive/6/6-4.pdf',
    'utah_r4': 'https://regulations.utah.edu/research/revisions_7/7-002.r4.pdf',
    'hawaii1985': 'https://www.hawaii.edu/policy/archives/ep/e5/e5500.pdf',
    'hawaii_current': 'https://www.hawaii.edu/policy/index.php?action=viewPolicy&menuView=closed&policyChapter=12&policyNumber=205&policySection=ep',
    'hawaii2020': 'https://www.hawaii.edu/policy/ep/12/205/ep12.205.pdf',
    'hawaii_cba2009': 'https://www.hawaii.edu/offices/app/personnel/2009-2015_AGREEMENT.pdf',
    'hawaii_cba2003': 'https://hilo.hawaii.edu/uhh/accreditation/documents/2003-2009BU7AGREEMENT_2.pdf',
}

def main():
    target = ROOT/'input/revisions'; target.mkdir(parents=True, exist_ok=True)
    logs = []
    for key, url in SOURCES.items():
        row = dict(source_id=key, url=url, retrieved_at=datetime.now(timezone.utc).isoformat())
        try:
            r = requests.get(url, timeout=40); row.update(status=r.status_code, resolved_url=r.url)
            r.raise_for_status()
            suffix = '.pdf' if r.content.startswith(b'%PDF') else '.docx' if r.content.startswith(b'PK') else '.html'
            p = target/(key+suffix); p.write_bytes(r.content)
            row.update(sha256=hashlib.sha256(r.content).hexdigest(), local_path=str(p.relative_to(ROOT)))
            if suffix == '.pdf':
                subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
            elif suffix == '.docx':
                with zipfile.ZipFile(p) as z:
                    tree = ET.fromstring(z.read('word/document.xml'))
                    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                    paragraphs = [''.join(n.itertext()) for n in tree.findall('.//w:p', ns)]
                    p.with_suffix('.txt').write_text('\n'.join(paragraphs))
            else:
                from html.parser import HTMLParser
                class Extract(HTMLParser):
                    def __init__(self): super().__init__(); self.parts=[]
                    def handle_data(self, data): self.parts.append(data)
                parser=Extract(); parser.feed(r.text)
                p.with_suffix('.txt').write_text('\n'.join(parser.parts))
            row['interpretation_status'] = 'retrieved_not_authenticated'
        except Exception as e:
            row['error'] = str(e)
        logs.append(row); print(key, row.get('status'), row.get('error',''))
    (ROOT/'results/revision_source_retrieval.json').write_text(json.dumps(logs,indent=2)+'\n')

if __name__ == '__main__': main()
