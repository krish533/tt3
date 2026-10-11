"""Build bibliography and field-level audit from checked metadata and explicit overrides.

No network; metadata retrieval and substantive checking are separate operations.
Rejected DOI search hits remain in metadata/ for an auditable correction trail.
"""
import csv,json,re,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-10'

def tex(s):
    return html.unescape(str(s)).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')

def page_range(s):
    parts=s.split('-')
    if len(parts)!=2 or not all(v.isdigit() for v in parts):return s
    a,b=parts
    if len(a)!=len(b):return a+'--'+b
    i=0
    while i<min(len(a),len(b))-2 and a[i]==b[i]:i+=1
    return a+'--'+b[i:]

def main():
    records=[]
    for seed in csv.DictReader((ROOT/'references/search_seeds.tsv').open(),delimiter='\t'):
        k=seed['citekey'];m=json.loads((ROOT/f'references/metadata/{k}.json').read_text())
        a=m.get('author') or []
        r=dict(key=k,type='book' if k in ['hart1995','north1990','nrc2011'] else 'article',
          title=seed['expected_title'],authors=[{'family':v.get('family',''),'given':v.get('given','')} for v in a],
          year=m['published']['date-parts'][0][0],journal=(m.get('container-title') or [''])[0],
          publisher=m.get('publisher') or '',volume=m.get('volume') or '',issue=m.get('issue') or '',
          pages=m.get('page') or m.get('article-number') or '',doi=m.get('DOI') or '',url=seed['primary_url'],
          claim=seed['claim_supported'],verification='publisher_metadata_and_primary_page_checked',
          content_scope='abstract_or_primary_summary; limited claim only; not full-text review',corrections='')
        if k in ['dreyfuss1987','eisenberg1996','fisk1998']:
            r['pages']={'dreyfuss1987':'590-647','eisenberg1996':'1663-1727','fisk1998':'1127-1198'}[k]
            r['corrections']='Crossref only supplied first page; range checked against institutional/publisher record.'
        if k=='rai2003':
            r.update(authors=[{'family':'Rai','given':'Arti K.'},{'family':'Eisenberg','given':'Rebecca S.'}],year=2003,journal='Law and Contemporary Problems',volume='66',issue='1/2',pages='289-314',doi='',corrections='Rejected SSRN 2002 hit; official journal version used; no original-journal DOI located.')
        if k=='reichman2003':
            r.update(authors=[{'family':'Reichman','given':'J. H.'},{'family':'Uhlir','given':'Paul F.'}],year=2003,journal='Law and Contemporary Problems',volume='66',issue='1/2',pages='315-462',doi='',corrections='Rejected 2016 anthology DOI; official original journal version used; no original-journal DOI located.')
        if k=='rai1999':
            r.update(authors=[{'family':'Rai','given':'Arti K.'}],year=1999,journal='Northwestern University Law Review',volume='94',issue='1',pages='77-152',doi='',corrections='SSRN DOI is a working-paper identifier, not an original journal DOI; omitted.')
        if k=='nrc2011':
            r.update(authors=[{'family':'National Research Council','given':''}],year=2011,publisher='National Academies Press',corrections='Official frontmatter publication year 2011 overrides anomalous Crossref 2010 date.')
        if k=='hart1995':r['publisher']='Oxford University Press'
        r['journal']=html.unescape(r['journal'])
        if k=='wilkinson2016':r.update(pages='160018',issue='')
        if k in ['north1990','fisk1998','kenney2011']:
            r['corrections']+=' Rejected first title-search hit (later chapter/reprint/working paper); replaced with original DOI.'
        if k in ['murray2007','berman2008']:r['corrections']+=' Restored subtitle from primary publication page.'
        if k=='halilem2017':
            r['content_scope']='Author institutional bibliography verifies metadata; publisher abstract available through index; full text inaccessible.'
            r['verification']='metadata_verified_substantive_full_text_pending'
        if k=='dasgupta1994':
            r['authors'][0]={'family':'Dasgupta','given':'Partha'}
            r['corrections']+=' Crossref reverses first author given/family names; corrected against author CV.'
            r['content_scope']='Author CV confirms original bibliographic record; abstract and later author-repository version support broad framework only.'
        if k=='jamali2024':r['content_scope']='Primary full text, Methods and Results checked.'
        records.append(r)
    # Primary sources have no journal DOI requirement. Statutory date is the cited edition.
    manual=[
      ('palmer1962','Archie M.','Palmer',1962,'University Research and Patent Policies, Practices and Procedures','National Academy of Sciences--National Research Council, Publication 999','https://files.eric.ed.gov/fulltext/ED054714.pdf','Contemporaneous patent-policy survey; Caltech printed pp. 55–57 corroborate architecture, not exact 1945 wording.'),
      ('bayhdole2024','','United States Congress',2024,'Patent Rights in Inventions Made with Federal Assistance','35 U.S.C. §§ 200–212, 2024 edition','https://www.govinfo.gov/content/pkg/USCODE-2024-title35/html/USCODE-2024-title35-partII-chap18.htm','Election to retain title to subject inventions; not automatic inventor-to-university vesting.'),
      ('copyrightact','','United States Congress',1976,'Copyright Act of 1976, as amended','17 U.S.C. §§ 101–102, 201–202, 204; online consolidated text accessed 2026-10-10','https://www.copyright.gov/title17/','Authorship, work made for hire, material-object distinction and written transfer requirements; Chapters 1 and 2 checked.'),
      ('roche2011','','Supreme Court of the United States',2011,'Board of Trustees of the Leland Stanford Junior University v. Roche Molecular Systems, Inc.','563 U.S. 776–803','https://www.govinfo.gov/content/pkg/USREPORTS-563/pdf/USREPORTS-563-776.pdf','Bayh–Dole does not automatically vest title; majority pp. 785–789; assignment construction not reviewed, p. 785 n.2.'),
      ('dubilier1933','','Supreme Court of the United States',1933,'United States v. Dubilier Condenser Corp.','289 U.S. 178–224','https://www.govinfo.gov/content/pkg/USREPORTS-289/pdf/USREPORTS-289-178.pdf','Employee inventions and shop rights; pp. 187–189 distinguish hired-to-invent obligations.'),
      ('reid1989','','Supreme Court of the United States',1989,'Community for Creative Non-Violence v. Reid','490 U.S. 730–753','https://tile.loc.gov/storage-services/service/ll/usrep/usrep490/usrep490730/usrep490730.pdf','Common-law agency inquiry for copyright work made for hire; pp. 739–741, 751–753.'),
      ('feist1991','','Supreme Court of the United States',1991,'Feist Publications, Inc. v. Rural Telephone Service Co.','499 U.S. 340–364','https://tile.loc.gov/storage-services/service/ll/usrep/usrep499/usrep499340/usrep499340.pdf','Facts are not copyrightable; original selection/arrangement may be; pp. 344–351.'),
      ('usco2025','','United States Copyright Office',2025,'Copyright and Artificial Intelligence, Part 2: Copyrightability','U.S. Copyright Office, January 2025','https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf','Human authorship requirement; executive summary and conclusions; agency report, not legislation.'),
      ('isu2024','','Illinois State University',2024,'Intellectual Property Policy','Policy 4.1.10, revised May 2024','https://policy.illinoisstate.edu/academic/4-1-10/','Sections 2.8–2.12 and 3.1–3.3: resources, academic works, student rights, differentiated ownership.'),
      ('wfu2006','','Wake Forest University',2006,'Patent Policy','February 1999 adoption history; retrieved reprint bears 26 May 2006 amendment','https://prod.wp.cdn.aws.wfu.edu/sites/193/2014/02/WFU-Patent-Policy.pdf','Sections 2 and 4: patentable/nonpatentable inventions, device-like software, conditional ownership; not an authenticated pristine 1999 version.'),
      ('wfu2017','','Wake Forest University',2017,'Intellectual Property Policy, Reynolda Campus','Effective 6 October 2017','https://prod.wp.cdn.aws.wfu.edu/sites/193/2018/11/Reynolda-Campus-IP-Policy.pdf','Sections 3.1–3.4 and 4.2: assignment, nonemployee students, traditional scholarship and retained rights.'),
      ('creighton2019','','Creighton University',2019,'Intellectual Property Policy','Policy 4.2.3, revised 22 April 2019','https://www.creighton.edu/sites/default/files/2022-01/4-2-3-Intellectual-Property-rev-4-22-19.pdf','Sections C, D.2 and Appendix I: conditional ownership, reciprocal license, exclusions and assignment form.')]
    for k,g,f,y,t,p,u,c in manual:
        records.append(dict(key=k,type='book' if k=='palmer1962' else 'misc',title=t,authors=[dict(family=f,given=g)],year=y,journal='',publisher=p,volume='',issue='',pages='',doi='',url=u,claim=c,verification='primary_source_relevant_passages_checked',content_scope='Named provisions/passages inspected; no independent human legal review.',corrections='No DOI applicable or located.'))
    records.sort(key=lambda r:(tuple(a['family'].lower() for a in r['authors']),r['year'],r['key']))
    bib=[]; rendered=[]; audit=[]
    for r in records:
        authors=r['authors']; names=[]
        for a in authors:
            if a['given']:
                initials=' '.join(w[0]+'.' for w in a['given'].split() if w)
                names.append(a['family']+', '+initials)
            else:names.append(a['family'])
        display=(names[0] if len(names)==1 else ', '.join(names[:-1])+' and '+names[-1]) if len(names)<=3 else ', '.join(names[:3])+', et al.'
        label=authors[0]['family']+(' and '+authors[1]['family'] if len(authors)==2 else ' et al.' if len(authors)>2 else '')
        authorbib=' and '.join((a['family']+', '+a['given']) if a['given'] else '{'+a['family']+'}' for a in authors)
        fields=dict(author=authorbib,title='{'+tex(r['title'])+'}',year=r['year'])
        if r['type']=='article':fields.update(journal=tex(r['journal']),volume=r['volume'],number=r['issue'],pages=r['pages'].replace('-','--'))
        else:fields['publisher' if r['type']=='book' else 'howpublished']=tex(r['publisher'])
        fields.update(doi=r['doi'],url=r['url'])
        bib.append('@'+r['type']+'{'+r['key']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields.items() if str(v))+'\n}')
        if r['type']=='article':
            details="`"+tex(r['title'])+"', \\emph{"+tex(r['journal'])+'}, '+r['volume']+('('+r['issue']+')' if r['issue'] else '')+': '+page_range(r['pages'])+'.'
        else:details=r'\emph{'+tex(r['title'])+'}. '+tex(r['publisher'])+'.'
        link='https://doi.org/'+r['doi'] if r['doi'] else r['url']
        rendered.append(r'\bibitem['+tex(label)+'('+str(r['year'])+')]{'+r['key']+'} '+tex(display)+' ('+str(r['year'])+'). '+details+r' \url{'+link+'}.')
        audit.append({k:r[k] for k in ['key','title','year','journal','publisher','volume','issue','pages','doi','url','claim','verification','content_scope','corrections']}|{'authors':'; '.join((a['given']+' '+a['family']).strip() for a in authors),'checked_on':DATE,'checker':'AI-assisted source comparison; no independent human verifier','metadata_cache':f"references/metadata/{r['key']}.json" if (ROOT/f"references/metadata/{r['key']}.json").exists() else 'primary source linked','issue_pages_status':'article fields checked; book/statute/report/case fields not journal-applicable'})
    (ROOT/'references/references.bib').write_text('\n\n'.join(bib)+'\n')
    (ROOT/'references/references.tex').write_text('\\begin{thebibliography}{99}\n'+ '\n\n'.join(rendered)+'\n\\end{thebibliography}\n')
    with (ROOT/'references/reference_audit.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(audit[0]),lineterminator='\n');w.writeheader();w.writerows(audit)
    (ROOT/'references/accepted_records.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    print('Bibliography records:',len(records))

if __name__=='__main__':main()
