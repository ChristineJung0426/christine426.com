// Keep enlargement available; discourage ordinary save/drag gestures only.
(() => {
  const overlay = document.createElement('div');
  overlay.className = 'art-lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Artwork preview');
  overlay.innerHTML = '<button type="button" aria-label="Close image">×</button><img alt="" draggable="false">';
  document.body.append(overlay);
  let returnFocus;
  const close = () => { overlay.classList.remove('open'); document.body.style.overflow = ''; returnFocus?.focus(); };
  const show = image => {
    returnFocus = document.activeElement;
    const large = overlay.querySelector('img'); large.src = image.currentSrc || image.src; large.alt = image.alt;
    overlay.classList.add('open'); document.body.style.overflow = 'hidden'; overlay.querySelector('button').focus();
  };
  document.querySelectorAll('.gallery-item img, .carousel-slide img, .project-cover img, .media img, a[data-lightbox] img').forEach(img => {
    img.draggable = false; img.tabIndex = 0;
    img.addEventListener('click', e => { e.preventDefault(); show(img); });
    img.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(img); } });
  });
  overlay.addEventListener('click', e => { if (e.target.tagName !== 'IMG') close(); });
  document.addEventListener('keydown', e => {
    if (!overlay.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'Tab') { e.preventDefault(); overlay.querySelector('button').focus(); }
  });
  for (const event of ['contextmenu','dragstart']) document.addEventListener(event, e => {
    if (e.target.closest('img, video, .gallery-item, .art-lightbox, a[data-lightbox]')) e.preventDefault();
  });
  document.querySelectorAll('video').forEach(v => v.setAttribute('controlsList','nodownload'));
  const nav = document.querySelector('.project-nav');
  if (nav) window.addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 20), {passive:true});
})();
