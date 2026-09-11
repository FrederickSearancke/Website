"""Audit rendered project prose against the original PDF text and block register."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
from authored import DATA, original, norm, APPROVED_EDITS

ROOT=Path(__file__).resolve().parent
class Node:
    def __init__(self,tag='',attrs=None,parent=None):
        self.tag=tag;self.attrs=dict(attrs or []);self.parent=parent;self.children=[]
    def text(self):
        return ''.join(x.text() if isinstance(x,Node) else x for x in self.children)
    def nodes(self):
        yield self
        for c in self.children:
            if isinstance(c,Node):yield from c.nodes()
    def within(self,cls):
        n=self
        while n:
            if cls in n.attrs.get('class','').split():return True
            n=n.parent
        return False
    def unsourced(self):
        if 'data-source-blocks' in self.attrs:return ''
        return ''.join(x.unsourced() if isinstance(x,Node) else x for x in self.children)

class Tree(HTMLParser):
    def __init__(self):
        super().__init__();self.root=Node();self.current=self.root
    def handle_starttag(self,tag,attrs):
        n=Node(tag,attrs,self.current);self.current.children.append(n)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.current=n
    def handle_endtag(self,tag):
        n=self.current
        while n.parent and n.tag!=tag:n=n.parent
        if n.parent:self.current=n.parent
    def handle_data(self,text):self.current.children.append(text)

def compact(text):return re.sub(r'\s+','',text)

def main():
    errors=[];verified=0;approved_count=0;unique=set();pages=[];pdf_checks=[]
    from pypdf import PdfReader
    for d in DATA['documents']:
        path=Path(d['original_path'])
        if hashlib.sha256(path.read_bytes()).hexdigest()!=d['source_sha256']:
            errors.append(f'Source PDF changed: {path.name}');continue
        reader=PdfReader(path)
        original_chars=compact(' '.join(p.extract_text() or '' for p in reader.pages))
        for b in DATA['blocks']:
            if b['document_key']==d['document_key'] and compact(b['text']) not in original_chars:
                errors.append(f'Source block not present in PDF: {b["block_id"]}')
        pdf_checks.append({'document':d['document_key'],'pages':len(reader.pages),'sha256_verified':True})
    for file in sorted((ROOT/'dist').rglob('index.html')):
        parser=Tree();parser.feed(file.read_text(encoding='utf-8'));nodes=list(parser.root.nodes());count=0
        for n in nodes:
            ids=n.attrs.get('data-source-blocks')
            if ids:
                block_ids=ids.split()
                expected, expected_ids=original(block_ids[0])
                if expected_ids != block_ids:errors.append(f'{file}: wrong paragraph continuation IDs')
                actual=norm(n.text())
                if n.attrs.get('data-approved-edit'):
                    edit=APPROVED_EDITS.get(n.attrs['data-approved-edit'],{})
                    replacement=norm(edit.get('replacement',''))
                    matches_copy=(bool(actual) and actual in replacement) if n.attrs.get('data-approved-excerpt')=='true' else actual==replacement
                    valid=edit.get('source_block')==block_ids[0] and norm(edit.get('original',''))==expected and matches_copy
                    approved_count+=1
                else:
                    valid=actual in expected if n.attrs.get('data-source-excerpt')=='true' else actual==expected
                if not valid:errors.append(f'{file}: altered author wording in {ids}')
                verified+=1;count+=1;unique.update(block_ids)
            # Project prose is either a tagged paragraph or a container for a tagged excerpt.
            if n.tag in {'p','li','blockquote'} and (n.within('article') or n.within('project-copy') or ('projects' in file.relative_to(ROOT/'dist').parts and n.within('project-hero') and n.within('lede'))):
                if norm(n.unsourced()):errors.append(f'{file}: untracked project prose: {n.unsourced()[:100]}')
        pages.append({'page':str(file.relative_to(ROOT/'dist')).replace('\\','/'),'source_text_elements':count})
        for n in nodes:
            if n.tag=='footer' and '2026' in n.text():errors.append(f'{file}: footer year remains')
            if n.tag in {'a','div'} and norm(n.text())=='FS':errors.append(f'{file}: initials placeholder remains')
        if file==ROOT/'dist/skills/index.html':
            groups=[n for n in nodes if 'skill-group' in n.attrs.get('class','').split()]
            if [sum(c.tag=='li' for c in g.nodes()) for g in groups] != [3,4,3,4]:errors.append('Skills must retain the existing 3 / 4 / 3 / 4 entries across four groups')
            if any(term in ' '.join(g.text() for g in groups).lower() for term in ['blender automation','graph traversal','stacks and backtracking','vector similarity']):errors.append('An excluded skill remains')
        if file==ROOT/'dist/index.html':
            if '01 — 03' in parser.root.text() or 'From the work' in parser.root.text():errors.append('Removed homepage labels remain')
    result={'passed':not errors,'source_pdfs_checked':pdf_checks,'rendered_source_elements_verified':verified,'verbatim_source_elements':verified-approved_count,'explicitly_approved_copy_edits':approved_count,'unique_source_blocks_used':len(unique),'pages':pages,'allowed_editorial_changes':['Display titles and navigation labels','Short figure labels and alt text; source captions preserved where available','Paragraph placement, before/after comparison layout and whitespace','Stat labels; coursework scores supplied directly by Frederick on 10 September 2026','Skills labels based on the user request, Desktop source and LinkedIn','Explicit copy edits recorded in content/approved-edits.json'],'errors':errors}
    (ROOT/'content/wording-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Checked {len(pdf_checks)} source PDFs, {sum(x["pages"] for x in pdf_checks)} pages, {verified} rendered source elements and {len(unique)} distinct source blocks.')
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    print(f'Author wording matches: {verified-approved_count} exact source elements and {approved_count} explicit user-approved edit(s). Layout checks passed.')
if __name__=='__main__':main()
