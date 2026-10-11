"""Create a replication archive and check deterministic output hashes."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def files():
 names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
 return sorted({ROOT/n for n in names if n!='deliverables/paper3-replication.zip' and (ROOT/n).is_file()})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
 manifest=ROOT/'replication/output_checksums.json'
 if a.check:
  for rel,sha in json.loads(manifest.read_text()).items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==sha,rel
  print('Deterministic output checksums verified');return
 selected=[p for p in files() if (p.parent==ROOT/'results' and p.suffix in ['.csv','.json'] and 'retrieval_log' not in p.name and p.name not in ['release_verification.json']) or p.relative_to(ROOT).as_posix() in ['references/references.bib','references/references.tex','deliverables/paper3-word.rtf']]
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in selected}
 manifest.write_text(json.dumps(hashes,indent=2)+'\n')
 with zipfile.ZipFile(ROOT/'deliverables/paper3-replication.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in files():
   info=zipfile.ZipInfo(str(p.relative_to(ROOT)),date_time=(2000,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,p.read_bytes())
 print('Replication ZIP created; output hashes:',len(hashes))
if __name__=='__main__':main()
