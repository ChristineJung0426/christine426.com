# christine426.com

Static rebuild of the original Creatorlink site (same design), hosted on GitHub Pages.

## Structure
- `index.html`, `photography.html`, `resume.html`, `demo-reel.html`, `projects/*.html` — the built site
- `style.css`, `site.js` — all styling and behavior (carousel, lightbox, mobile menu)
- `images/web/` — web-sized images used by the site
- `images/src/` — full-resolution originals (not uploaded; see .gitignore)
- `_build/content.py` — **all page content lives here** (home cards, project text, image and video order)
- `_build/build.py` — regenerates every HTML page from content.py

## Making changes
1. Edit `_build/content.py` (text, order, YouTube ids) or `style.css` (look).
2. Run `python3 _build/build.py` from this folder.
3. Commit and push; GitHub Pages updates in about a minute.

To add a project: put its images in `images/src/`, add a card to `HOME` and a page to `PAGES` in content.py, then rebuild.

## Design values (measured from the original site, 2026-10-28)
Background #050505 · text #F5F5F5 / #EBE8EB · logo Lora 700 16px, letter-spacing .15em ·
nav Lora 12px, letter-spacing .3em, active item struck through · home grid full-bleed 2 columns, 2:1, no gap ·
hover: black 70% overlay + centered title (15px) and caption (13px), 0.4s ease-in-out ·
project pages: 1140px column, 50px between media, section headings Nanum Gothic 17px bold.
