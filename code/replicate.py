"""Single deterministic analytical pipeline; optional PDF compilation.
Network only for absent immutable source inputs. Policy retrieval is separate.
"""
import argparse,hashlib,json,os,platform,subprocess,sys
from importlib.metadata import version
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args):subprocess.run([sys.executable,*args],cwd=ROOT,check=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--pdf',action='store_true');a=ap.parse_args()
 os.environ['MPLCONFIGDIR']=str(ROOT/'build/matplotlib');os.environ['SOURCE_DATE_EPOCH']='1791586800'
 run('code/fetch_sources.py')
 run('code/extract_ownership.py','input/policy_sentences_cleaned_combined.csv')
 run('code/analyze_screening.py')
 for name in ['audit_corpus','classify_provisions','analyze_history','recover_embedded_sources','build_evidence','analyze_substantive_transitions','build_references','build_tables','audit_manuscript','sync_overleaf','export_word_rtf']:
  run('code/'+name+'.py')
 run('-m','unittest','discover','-s','tests','-v')
 (ROOT/'build').mkdir(exist_ok=True)
 (ROOT/'build/runtime.json').write_text(json.dumps(dict(python=sys.version,platform=platform.platform(),packages={p:version(p) for p in ['pandas','numpy','matplotlib','requests']}),indent=2)+'\n')
 if a.pdf:
  subprocess.run(['tectonic','--keep-logs','--keep-intermediates','--outdir',str(ROOT/'build'),'main.tex'],cwd=ROOT/'overleaf',check=True)
  import shutil
  shutil.copyfile(ROOT/'build/main.pdf',ROOT/'deliverables/paper3.pdf')
 print('Replication completed. Legal validation remains incomplete; see docs/submission_readiness.md.')
if __name__=='__main__':main()
