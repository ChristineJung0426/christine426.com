// Carousels
document.querySelectorAll('.carousel').forEach(c => {
  const track = c.querySelector('.track'), n = track.children.length, dots = c.querySelector('.dots');
  let i = 0;
  for (let k = 0; k < n; k++) { const d = document.createElement('i'); d.onclick = () => go(k); dots.appendChild(d); }
  function go(k) { i = (k + n) % n; track.style.transform = `translateX(-${i * 100}%)`; [...dots.children].forEach((d, j) => d.classList.toggle('on', j === i)); }
  c.querySelector('.prev').onclick = () => go(i - 1);
  c.querySelector('.next').onclick = () => go(i + 1);
  go(0);
});
// Lightbox for project and photography images
const lb = document.createElement('div'); lb.className = 'lb'; lb.innerHTML = '<img alt="">'; document.body.appendChild(lb);
lb.onclick = () => lb.classList.remove('on');
document.addEventListener('keydown', e => { if (e.key === 'Escape') lb.classList.remove('on'); });
document.querySelectorAll('.media img, a[data-lightbox]').forEach(el => {
  el.style.cursor = 'zoom-in';
  el.addEventListener('click', e => { e.preventDefault(); lb.querySelector('img').src = el.tagName === 'A' ? el.href : el.src; lb.classList.add('on'); });
});
