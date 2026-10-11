"""Word-compatible RTF from this manuscript's limited LaTeX vocabulary.

No DOCX/LibreOffice dependency. Word rendering still requires external visual QA.
Fails on unhandled commands instead of silently dropping substantive text.
"""
import json,re
from pathlib import Path
from build_references import page_range
ROOT=Path(__file__).resolve().parents[1]
REFS={r['key']:r for r in json.loads((ROOT/'references/accepted_records.json').read_text())}
MACROS=dict(re.findall(r'\\newcommand\{\\(\w+)\}\{([^}]+)\}',(ROOT/'manuscript/numbers.tex').read_text()))
LABELS={'tab:population':'1','tab:decades':'2','tab:transitions':'3','tab:weighted':'4','tab:sensitivity':'5','tab:readings':'6','fig:coverage':'1'}
def citation(m):
 kind,extra,keys=m.groups();values=[]
 for key in keys.split(','):
  r=REFS[key];a=r['authors'];name=a[0]['family']+(' and '+a[1]['family'] if len(a)==2 else ' et al.' if len(a)>2 else '')
  values.append(name+' ('+str(r['year'])+')' if kind=='t' else name+', '+str(r['year']))
 s='; '.join(values)+((', '+extra) if extra else '')
 return s if kind=='t' else '('+s+')'
def plain(s):
 s=re.sub(r'\\cite([pt])(?:\[([^\]]+)\])?\{([^}]+)\}',citation,s)
 for k,v in MACROS.items():s=s.replace('\\'+k+'{}',v)
 s=re.sub(r'\\ref\{([^}]+)\}',lambda m:LABELS[m[1]],s)
 s=re.sub(r'\\label\{[^}]+\}','',s)
 for _ in range(3):s=re.sub(r'\\(?:textit|emph|url)\{([^{}]*)\}',r'\1',s)
 s=re.sub(r'\\(?:noindent|smallskip|footnotesize|raggedright|centering|small|par)','',s)
 s=s.replace('\\&','&').replace('~',' ').replace('---','—').replace('--','–').replace('\\%','%')
 if re.search(r'\\[a-zA-Z]+',s):raise ValueError('Unhandled LaTeX: '+s[:200])
 return ' '.join(s.split())
def esc(s):
 out=[]
 for c in s:
  n=ord(c)
  if c in '\\{}':out.append('\\'+c)
  elif n>127:out.append('\\u'+str(n if n<32768 else n-65536)+'?')
  else:out.append(c)
 return ''.join(out)
def para(s,bold=False,size=24,center=False):
 return r'\pard\widctlpar\sa100\sl300\slmult1'+(r'\qc' if center else r'\ql')+'\\fs'+str(size)+(r'\b ' if bold else ' ')+esc(s)+(r'\b0' if bold else '')+r'\par'+'\n'
def rows_rtf(rows):
 n=len(rows[0]); widths=([2600,5900,9360] if n==3 else [5000,6090,7180,8270,9360] if n==5 else [4500,5700,6900,9360] if n==4 else [1100,2600,4200,6100,7600,9360] if n==6 else [7500,9360])
 out=[]
 for i,row in enumerate(rows):
  assert len(row)==n
  out.append(r'\trowd\trgaph100\trleft0'+(r'\trhdr' if i==0 else '')+''.join('\\cellx'+str(v) for v in widths))
  for cell in row:out.append(r'\pard\intbl\ql\fs20 '+(r'\b ' if i==0 else '')+esc(plain(cell))+(r'\b0' if i==0 else '')+r'\cell')
  out.append(r'\row')
 return '\n'.join(out)+'\n'
def main():
 text=(ROOT/'manuscript/main.tex').read_text()
 status=plain(re.search(r'\\noindent (Research status:.*?)\\newpage',text,re.S)[1])
 body=text.split('\\begin{abstract}',1)[1].split('\\begingroup',1)[0]
 body='\\section*{Abstract}\n'+body.replace('\\end{abstract}','')
 blocks=re.split(r'(\\begin\{table\}.*?\\end\{table\}|\\begin\{figure\}.*?\\end\{figure\}|\\section\*?\{[^}]+\})',body,flags=re.S)
 output=[r'{\rtf1\ansi\deff0{\fonttbl{\f0 Times New Roman;}}\paperw12240\paperh15840\margl1440\margr1440\margt1440\margb1440\f0',para('Who Owns Academic Knowledge?',True,32,True),para('The Evolution of Intellectual Property Rights in American Universities',True,30,True),para('Anonymous research manuscript',center=True),para('10 October 2026',center=True),para('Historical policy evidence, legal distinctions, and limits of identification',center=True),para('Approximate total word count: 6,500, including tables and references',center=True),para(status),r'\page']
 table_no=0;section_no=0
 for b in blocks:
  if not b.strip():continue
  if b.startswith('\\section'):
   title=re.search(r'\{([^}]+)\}',b)[1]
   if not b.startswith('\\section*'):section_no+=1;title=str(section_no)+' '+title
   output.append(para(title,True,28));continue
  if b.startswith('\\begin{table}'):
   table_no+=1;caption=re.search(r'\\caption\{([^}]+)\}',b)[1]
   output.append(para('Table '+str(table_no)+': '+caption,True,22))
   inp=re.search(r'\\input\{([^}]+)\}',b)
   source=(ROOT/'manuscript'/inp[1]).read_text() if inp else b
   tabletext=source.split('\\toprule',1)[1].split('\\bottomrule',1)[0].replace('\\midrule','')
   rows=[[c.strip() for c in row.split('&')] for row in tabletext.split('\\\\') if row.strip()]
   output.append(rows_rtf(rows))
   note=b.rsplit('\\raggedright',1)[1].split('\\end{table}',1)[0]
   output.append(para(plain(note),size=20));continue
  if b.startswith('\\begin{figure}'):
   png=(ROOT/'manuscript/figures/archival_coverage.png').read_bytes()
   output.append(r'\pard\qc{\pict\pngblip\picw1260\pich630\picwgoal9000\pichgoal4500 '+png.hex()+r'}\par')
   output.append(para('Figure 1: '+re.search(r'\\caption\{([^}]+)\}',b)[1],size=22));continue
  for p in re.split(r'\n\s*\n',b):
   if p.strip():output.append(para(plain(p)))
 output.append(para('References',True,28))
 for r in REFS.values():
  names=[]
  for a in r['authors']:
   names.append(a['family']+(', '+ ' '.join(w[0]+'.' for w in a['given'].split()) if a['given'] else ''))
  name=(names[0] if len(names)==1 else ', '.join(names[:-1])+' and '+names[-1]) if len(names)<=3 else ', '.join(names[:3])+', et al.'
  detail=(r['journal']+', '+r['volume']+('('+r['issue']+')' if r['issue'] else '')+': '+page_range(r['pages']).replace('--','–')) if r['type']=='article' else r['publisher']
  link='https://doi.org/'+r['doi'] if r['doi'] else r['url']
  output.append(para(name+' ('+str(r['year'])+'). '+r['title']+'. '+detail+'. '+link+'.',size=21))
 output.append('}')
 target=ROOT/'deliverables/paper3-word.rtf';target.write_text('\n'.join(output),encoding='ascii')
 (ROOT/'results/word_export_audit.json').write_text(json.dumps(dict(format='rtf',source='manuscript/main.tex',tables=table_no,figures=1,bibliography_entries=len(REFS),unsupported_latex_commands=0,visual_render_verified=False,limitation='No bundled document runtime/LibreOffice renderer exposed. RTF is Word-compatible; final Word pagination must be inspected externally.'),indent=2)+'\n')
 print(target)
if __name__=='__main__':main()
