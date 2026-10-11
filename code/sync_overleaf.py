"""Create/check a self-contained mirror; main.tex is always byte-identical.
Do not edit overleaf/: edit manuscript/ or references/ and regenerate.
"""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mapping():
 files={p.relative_to(ROOT/'manuscript'):p for p in (ROOT/'manuscript').rglob('*') if p.is_file() and p.suffix in ['.tex','.pdf','.png'] and p.name!='main.pdf'}
 for name in ['references.bib','references.tex']:
  files[Path('references')/name]=ROOT/'references'/name
 return files

def sync(check=False):
 target=ROOT/'overleaf';target.mkdir(exist_ok=True)
 files=mapping();manifest={}
 for rel,p in sorted(files.items()):
  dest=target/rel
  if check:
   assert dest.exists() and dest.read_bytes()==p.read_bytes(),f'Mirror divergence: {rel}'
  else:
   dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
  manifest[str(rel)]=hashlib.sha256(p.read_bytes()).hexdigest()
 if check:
  assert json.loads((target/'sync_manifest.json').read_text())==manifest
 else:
  (target/'sync_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
  (target/'README.txt').write_text('Generated from canonical manuscript/ and references/. Do not edit this mirror.\nUpload the ZIP through New Project > Upload Project in Overleaf; choose main.tex and XeLaTeX.\nNo online project was created or updated. Run python3 code/sync_overleaf.py after canonical edits.\n')
  out=ROOT/'deliverables';out.mkdir(exist_ok=True)
  with zipfile.ZipFile(out/'paper3-overleaf.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(target.rglob('*')):
    if p.is_file() and (p.relative_to(target) in files or p.name in ['sync_manifest.json','README.txt']):
     info=zipfile.ZipInfo(str(p.relative_to(target)),date_time=(2000,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
     z.writestr(info,p.read_bytes())
 print('Overleaf mirror verified' if check else 'Overleaf mirror and ZIP generated')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');sync(ap.parse_args().check)
