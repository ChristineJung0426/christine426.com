import os, re, json, glob, html, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from content import HOME, PAGES, MATERIALS, INTRO, THUMBS, META
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
names = json.load(open('_source/names.json'))
smap = json.load(open('_source/map.json'))
srcfiles = {os.path.splitext(os.path.basename(f))[0]: f for f in glob.glob('images/src/*.*')}
def file_for_base(base): return srcfiles[names[base]]
def file_for_suffix(suf):
    hits = [b for b in names if b.endswith(suf)]
    assert len(hits) == 1, (suf, len(hits))
    return file_for_base(hits[0])

os.makedirs('images/web', exist_ok=True)
def web(src, maxw=2280):
    """Make a web-sized copy; returns path relative to site root."""
    stem = os.path.splitext(os.path.basename(src))[0]
    if src.lower().endswith('.gif'):
        out = f'images/web/{stem}.gif'
        if not os.path.exists(out): shutil.copy2(src, out)
        return out
    out = f'images/web/{stem}.jpg'
    if not os.path.exists(out):
        im = Image.open(src)
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (5, 5, 5)); bg.paste(im, mask=im.split()[-1]); im = bg
        else: im = im.convert('RGB')
        if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
        im.save(out, quality=86, optimize=True, progressive=True)
    return out
def dims(p):
    im = Image.open(p); return im.width, im.height

def fmt(text):
    """Plain text with **bold** and *italic* -> HTML paragraphs."""
    t = html.escape(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*([^*\n]+?)\*(?!\w)', r'<em>\1</em>', t)
    paras = [p for p in t.split('\n\n')]
    return ''.join(f'<p>{p.replace(chr(10), "<br>")}</p>' for p in paras if p.strip())

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;700&family=Abel&family=Nanum+Gothic:wght@400;700&family=Open+Sans:wght@400;700&family=Roboto:wght@400&display=swap" rel="stylesheet">'
         '<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">')
NAV = [('3D Art', 'index.html', 'home'), ('Demo Reel', 'demo-reel.html', 'reel'), ('Photography', 'photography.html', 'photo'), ('Resume', 'ChristineJung_Resume.pdf', 'resume')]
def page(title, body, active, depth=0, desc=''):
    up = '../' * depth
    ACT = ' class="active"'
    NEWTAB = ' target="_blank" rel="noopener"'
    nav = ''.join(f'<a href="{up}{href}"{ACT if key == active else ""}{NEWTAB if href.endswith(".pdf") else ""}>{label}</a>' for label, href, key in NAV)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, noimageindex">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc or 'Portfolio of Christine Jung. Specializing in immersive 3D environments, procedural generation, and PBR material authoring in Unreal Engine and Unity.')}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="Christine Jung — Technical Artist &amp; Environment Artist. Real-time environments, procedural tools, and PBR materials in Unreal Engine 5.">
<meta property="og:image" content="https://christine426.com/{OG_IMAGE}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}favicon.ico">
{FONTS}
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="{up}index.html">CHRISTINEJUNG</a>
    <button class="nav-toggle" aria-label="Menu" onclick="document.body.classList.toggle('nav-open')"><span></span><span></span><span></span></button>
    <nav class="site-nav">{nav}</nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="find-me"><span class="dash"></span><span>F I N D &nbsp; M E &nbsp; O N</span></div>
    <dl class="contact">
      <dt>Email</dt><dd><a href="mailto:christineart426@gmail.com">christineart426@gmail.com</a></dd>
      <dt>LinkedIn</dt><dd><a href="https://www.linkedin.com/in/christinejung426/" target="_blank" rel="noopener">linkedin.com/in/christinejung426</a></dd>
    </dl>
  </div>
</footer>
<a class="goto-top" href="#" aria-label="Back to top"></a>
<script src="{up}site.js"></script>
</body>
</html>
'''

# ---------- home ----------
def media_tag(w, title):
    if w.endswith('.mp4'):
        return f'<video src="{w}" autoplay muted loop playsinline aria-label="{html.escape(title)}"></video>'
    return f'<img src="{w}" alt="{html.escape(title)}" loading="lazy">'
OG_IMAGE = None
home_imgs = smap['pages']['home.html']['imgs']
k = 0; sections = []
OG_IMAGE = web(file_for_base(home_imgs[0]), 1600)
for si, (sec, items) in enumerate(HOME):
    cards = []
    for slug, title, cap, anchor in items:
        src = file_for_base(home_imgs[k]); k += 1
        w = THUMBS.get(title) or web(src, 1600)
        href = f'projects/{slug}.html' + (f'#{anchor}' if anchor else '')
        capline = f'<p class="cap">{cap}</p>' if cap else ''
        cards.append(f'<a class="card" href="{href}"><figure>{media_tag(w, title)}<figcaption><h5>{html.escape(title)}</h5>{capline}</figcaption></figure></a>')
    ncol = 3 if sec in ("Tech Art", "Materials") else 2
    divider = '' if si == len(HOME) - 1 else '<div class="wrap"><hr class="divider"></div>'
    sections.append(f'<section class="home-section"><div class="wrap"><h2 class="section-title">{html.escape(sec)}</h2></div><div class="grid cols-{ncol}">{"".join(cards)}</div>{divider}</section>')
intro = f'<div class="wrap"><p class="intro">{html.escape(INTRO)}</p></div>'
open('index.html', 'w').write(page('Christine Jung — Technical Artist & Environment Artist', intro + '\n'.join(sections), 'home'))

# ---------- project pages ----------
order = []
for _, items in HOME:
    for slug, *_ in items:
        if slug not in order: order.append(slug)
for slug, (t, f) in MATERIALS.items():
    imgs = [('I_BASE', b) for b in smap['pages'][f]['imgs']]
    seen = []; 
    for kind, b in imgs:
        if b not in seen: seen.append(b)
    PAGES[slug] = (t, [('I_BASE', b) for b in seen])
os.makedirs('projects', exist_ok=True)
def media_img(path):
    w, h = dims(path)
    return f'<figure class="media"><img src="../{path}" width="{w}" height="{h}" alt="" loading="lazy"></figure>'
for i, slug in enumerate(order):
    title, blocks = PAGES[slug]
    out = []
    for kind, val in blocks:
        if kind == 'T': out.append(f'<div class="desc">{fmt(val)}</div>')
        elif kind == 'H':
            first, _, rest = val.partition('\n')
            out.append(f'<div class="subhead"><h3>{html.escape(first)}</h3>{fmt(rest.strip()) if rest.strip() else ""}</div>')
        elif kind == 'A': out.append(f'<span class="anchor" id="{val}"></span>')
        elif kind == 'V': out.append(f'<figure class="media video"><iframe src="https://www.youtube-nocookie.com/embed/{val}" title="Video" loading="lazy" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></figure>')
        elif kind == 'I': out.append(media_img(web(file_for_suffix(val))))
        elif kind == 'I_BASE': out.append(media_img(web(file_for_base(val))))
        elif kind == 'IW': out.append(media_img(val))
        elif kind == 'VW': out.append(f'<figure class="media"><video src="../{val}" autoplay muted loop playsinline controls></video></figure>')
        elif kind == 'C':
            slides = ''.join(f'<img src="../{web(file_for_suffix(s))}" alt="" loading="lazy">' for s in val)
            out.append(f'<div class="carousel"><div class="track">{slides}</div><button class="prev" aria-label="Previous">&#8249;</button><button class="next" aria-label="Next">&#8250;</button><div class="dots"></div></div>')
    prev_s = order[i - 1] if i > 0 else None; next_s = order[i + 1] if i < len(order) - 1 else None
    pn = (f'<a class="pn prev" href="{prev_s}.html" aria-label="Previous project">&#8249;</a>' if prev_s else '<span class="pn disabled">&#8249;</span>') + \
         (f'<a class="pn next" href="{next_s}.html" aria-label="Next project">&#8250;</a>' if next_s else '<span class="pn disabled">&#8250;</span>')
    meta = ''.join(f'<div><dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd></div>' for a, b in META.get(slug, []))
    meta = f'<dl class="meta">{meta}</dl>' if meta else ''
    body = f'<article class="project wrap"><div class="project-top"><div><h1 class="project-title">{html.escape(title)}</h1>{meta}</div><div class="pager">{pn}</div></div>{"".join(out)}</article>'
    open(f'projects/{slug}.html', 'w').write(page(f'{title} — Christine Jung', body, 'home', 1))

# ---------- photography ----------
photos = sorted(glob.glob('images/src/photo/*'))
tiles = []
for p in photos:
    w = web(p, 1600)
    tiles.append(f'<a class="photo" href="{w}" data-lightbox><img src="{w}" alt="" loading="lazy"></a>')
open('photography.html', 'w').write(page('Photography — Christine Jung', f'<section class="wrap photo-page"><h2 class="section-title center">PHOTOGRAPHY</h2><div class="photo-grid">{"".join(tiles)}</div></section>', 'photo'))

# ---------- resume / demo reel ----------
res_base = smap['pages']['Resume.html']['imgs'][0]
rw = web(file_for_base(res_base))
open('resume.html', 'w').write(page('Euihyun Christine Jung', f'<section class="wrap single"><img class="resume" src="{rw}" alt="Resume of Euihyun Christine Jung"></section>', 'resume'))
open('demo-reel.html', 'w').write(page('Demo Reel — Christine Jung', '<section class="wrap single"><figure class="media video"><iframe src="https://www.youtube-nocookie.com/embed/ALanELcM4Jc" title="Demo reel" allowfullscreen></iframe></figure></section>', 'reel'))
print('built', len(order), 'project pages;', len(os.listdir('images/web')), 'web images')
