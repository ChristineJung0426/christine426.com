"""Build case studies using Python 3 standard library, without network access."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json, re

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / '_build/content.json').read_text(encoding='utf-8'))
template = (ROOT / '_build/project-template.html').read_text(encoding='utf-8')
e = lambda value: escape(str(value), quote=True)

def render(block, title, number):
    kind = block['type']
    text = e(block.get('text', ''))
    if kind == 'heading': return f'<div class="subhead"><h2>{text}</h2></div>'
    if kind == 'text': return f'<div class="desc"><p>{text}</p></div>'
    if kind == 'caption': return f'<p class="media-caption">{text}</p>'
    if kind == 'anchor': return f'<span class="anchor" id="{e(block["id"])}"></span>'
    if kind == 'link':
        href = block['href']
        for slug, page in data['pages'].items():
            if href.split('#')[0] == page.get('source'):
                href = slug + '.html' + ('#' + href.split('#',1)[1] if '#' in href else '')
                break
        return f'<p class="project-link"><a href="{e(href)}">{text}</a></p>'
    if kind in {'image', 'video'}:
        src = block['src']
        if not (ROOT / src).is_file(): raise FileNotFoundError(src)
        if kind == 'image':
            alt = e(block.get('alt') or f'{title} — project image {number}')
            return f'<figure class="media"><img src="../{e(src)}" alt="{alt}" loading="lazy" decoding="async"></figure>'
        return f'<figure class="media"><video src="../{e(src)}" muted loop playsinline controls preload="metadata" aria-label="{e(block.get("title", title))}"></video></figure>'
    if kind == 'embed':
        src = block['src']
        if urlsplit(src).hostname not in {'www.youtube-nocookie.com', 'www.youtube.com'}: raise ValueError(src)
        return f'<figure class="media video"><iframe src="{e(src)}" title="{e(block.get("title", title))}" loading="lazy" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></figure>'
    raise ValueError(kind)

for i, slug in enumerate(data['order']):
    layout = ROOT / '_build/layouts' / f'{slug}.html'
    if layout.exists():
        (ROOT/'projects'/f'{slug}.html').write_text(layout.read_text(encoding='utf-8'),encoding='utf-8')
        continue
    page = data['pages'][slug]
    title = page['title']
    meta = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in page['meta'])
    pager = []
    for offset, label, symbol in [(-1,'Previous','&#8249;'),(1,'Next','&#8250;')]:
        j = i+offset
        if 0 <= j < len(data['order']): pager.append(f'<a class="pn" href="{data["order"][j]}.html" aria-label="{label} project">{symbol}</a>')
    body = f'<article class="project wrap"><div class="project-top"><div><h1 class="project-title">{e(title)}</h1><dl class="meta">{meta}</dl></div><nav class="pager" aria-label="Projects">{"".join(pager)}</nav></div>'
    anchors = [b for b in page['blocks'] if b['type']=='anchor' and b['id'] in {'snow','icicle','ice-shader','snowflake','water'}]
    if anchors:
        labels={'snow':'Snow Generator','icicle':'Icicle Generator','ice-shader':'Ice Shader','snowflake':'Snowflake R&D','water':'Water Shaders'}
        body += '<nav class="project-sections" aria-label="On this page">' + ''.join(f'<a href="#{e(b["id"])}">{e(labels.get(b["id"],b["id"]))}</a>' for b in anchors) + '</nav>'
    body += '\n'.join(render(b,title,n+1) for n,b in enumerate(page['blocks']))
    body += '<p class="project-link"><a href="../index.html">← Back to all work</a></p></article>'
    output = template.replace('{{TITLE}}',e(title)).replace('{{CONTENT}}',body)
    desc = next((b['text'] for b in page['blocks'] if b['type']=='text'),title)
    output = re.sub(r'<meta name="description"[^>]*>',lambda _: f'<meta name="description" content="{e(desc)}">',output)
    (ROOT/'projects'/f'{slug}.html').write_text(output,encoding='utf-8')
print(f'Built {len(data["order"])} case studies. Homepage and other pages preserved.')
