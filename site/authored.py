"""Render the author's source text without rewriting it.

Only whitespace, paragraph boundaries and HTML presentation are normalised.
Every excerpt carries source-block IDs so the generated pages can be audited.
"""
from pathlib import Path
from html import escape
import json
import re

DATA = json.loads((Path(__file__).parent / 'content/source-blocks.json').read_text(encoding='utf-8'))
# New project PDFs keep their source text and extraction audit in separate bundles.
for supplemental in sorted((Path(__file__).parent / 'content/supplemental').glob('*.json')):
    DATA['blocks'].extend(json.loads(supplemental.read_text(encoding='utf-8'))['blocks'])
BLOCKS = {b['block_id']: b for b in DATA['blocks']}
APPROVED_EDITS = json.loads((Path(__file__).parent / 'content/approved-edits.json').read_text(encoding='utf-8'))

def norm(text):
    return re.sub(r'\s+', ' ', text).strip()

def original(block_id):
    ids = [block_id]
    text = BLOCKS[block_id]['text']
    while BLOCKS[ids[-1]].get('continues_in_block'):
        continuation = BLOCKS[ids[-1]]['continues_in_block']
        ids.append(continuation)
        text += ' ' + BLOCKS[continuation]['text']
    return norm(text).removeprefix('● '), ids

def author(block_id, tag='p', excerpt=None, cls=None):
    text, ids = original(block_id)
    if excerpt is not None:
        if norm(excerpt) not in text:
            raise ValueError(f'Excerpt does not match the author: {block_id}: {excerpt}')
        text = norm(excerpt)
    attrs = f' data-source-blocks="{" ".join(ids)}"'
    if excerpt is not None:
        attrs += ' data-source-excerpt="true"'
    if cls:
        attrs += f' class="{escape(cls)}"'
    return f'<{tag}{attrs}>{escape(text)}</{tag}>'

def paragraph_text(block_id):
    return original(block_id)[0]

def approved(edit_id, tag='span', excerpt=None):
    edit=APPROVED_EDITS[edit_id]
    text,ids=original(edit['source_block'])
    if norm(edit['original']) != text:
        raise ValueError(f'Approved edit source changed: {edit_id}')
    replacement = norm(edit['replacement'])
    excerpt_attr = ''
    if excerpt is not None:
        if not norm(excerpt) or norm(excerpt) not in replacement:
            raise ValueError(f'Excerpt does not match the approved edit: {edit_id}')
        replacement = norm(excerpt)
        excerpt_attr = ' data-approved-excerpt="true"'
    return f'<{tag} data-source-blocks="{" ".join(ids)}" data-approved-edit="{escape(edit_id)}"{excerpt_attr}>{escape(replacement)}</{tag}>'

def document(key, skip=(), before=None, after=None, overrides=None):
    before, after, overrides = before or {}, after or {}, overrides or {}
    output=[]
    listing=False
    for b in DATA['blocks']:
        bid=b['block_id']
        if b['document_key'] != key or bid in skip or b.get('continuation_of_block'):
            continue
        if b.get('heading_level') == 1 or b.get('caption_role') == 'alt_text':
            continue
        if b['kind'] == 'caption':
            continue
        is_list = b['kind'] == 'list'
        if listing and (not is_list or bid in before):
            output.append('</ul>');listing=False
        output.append(before.get(bid,''))
        if is_list and not listing:
            output.append('<ul>');listing=True
        if bid in overrides:
            output.append(overrides[bid])
        else:
            tag='li' if is_list else ('blockquote' if b['kind']=='example' else ('h3' if b.get('heading_level')==3 else ('h2' if b['kind']=='heading' else 'p')))
            output.append(author(bid,tag,cls='source-example' if tag=='blockquote' else None))
        if bid in after:
            if listing:
                output.append('</ul>');listing=False
            output.append(after[bid])
    if listing:
        output.append('</ul>')
    return ''.join(output)

def comparison(before_label, before_text, after_label, after_text):
    return '<div class="compare"><div>'+author(before_label,'p',cls='label')+author(before_text,'blockquote')+'</div><div class="after">'+author(after_label,'p',cls='label')+author(after_text,'blockquote')+'</div></div>'
