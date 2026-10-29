"""Check local links, anchor targets, case-study content and reproducible output."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import subprocess, sys, hashlib

ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.refs=[]; self.ids=[]; self.titles=0; self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.titles+=1
        for key in ['href','src']:
            if key in a: self.refs.append(a[key])

files=list(ROOT.glob('*.html'))+list((ROOT/'projects').glob('*.html'))
parsed={p:Links(p.read_text(encoding='utf-8')) for p in files}
errors=[]; checked=0
for p,doc in parsed.items():
    if len(doc.ids)!=len(set(doc.ids)): errors.append(f'Duplicate IDs: {p.name}')
    if p.parent.name=='projects' and doc.titles!=1: errors.append(f'Invalid h1 count: {p.name}')
    for ref in doc.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc: continue
        target=(p.parent/unquote(url.path)).resolve() if url.path else p
        checked+=1
        if not target.is_file(): errors.append(f'{p.name}: missing {ref}')
        elif url.fragment and target in parsed and unquote(url.fragment) not in parsed[target].ids: errors.append(f'{p.name}: missing anchor {ref}')
before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
subprocess.run([sys.executable,str(ROOT/'_build/build.py')],check=True)
if any(hashlib.sha256(p.read_bytes()).hexdigest()!=v for p,v in before.items()): errors.append('Build output is not reproducible')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(files)} HTML pages, {checked} local references, unique anchors, and reproducible build.')
