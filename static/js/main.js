// STICKY NAV
window.addEventListener('scroll', () => {
  document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
});

// MOBILE MENU
function toggleMenu(force) {
  const open = document.getElementById('mobileMenu').classList.toggle('open', force);
  document.getElementById('hamburger').classList.toggle('open', open);
}
document.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => toggleMenu(false)));
document.addEventListener('click', e => {
  if (!e.target.closest('#mobileMenu, #hamburger')) toggleMenu(false);
});
window.addEventListener('resize', () => { if (window.innerWidth > 900) toggleMenu(false); });

// DARK MODE (remembered across pages)
function applyDark(on) {
  document.body.classList.toggle('dark', on);
  const btn = document.getElementById('darkToggle');
  if (btn) btn.textContent = on ? '\u2600\uFE0F' : '\uD83C\uDF19';
}
function toggleDark() {
  const on = !document.body.classList.contains('dark');
  applyDark(on);
  try { localStorage.setItem('tog-dark', on ? '1' : '0'); } catch (e) {}
}
try { applyDark(localStorage.getItem('tog-dark') === '1'); } catch (e) {}

// SCROLL ANIMATIONS
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.aos').forEach(el => observer.observe(el));
setTimeout(() => {
  document.querySelectorAll('.aos:not(.visible)').forEach((el, i) => {
    setTimeout(() => el.classList.add('visible'), i * 80);
  });
}, 200);

// PARTICLES (home page only)
(function() {
  const container = document.getElementById('particles');
  if (!container || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  for (let i = 0; i < 20; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.left = Math.random() * 100 + '%';
    p.style.animationDuration = (8 + Math.random() * 14) + 's';
    p.style.animationDelay = (Math.random() * 12) + 's';
    p.style.setProperty('--dx', (Math.random() - 0.5) * 120 + 'px');
    container.appendChild(p);
  }
})();

// PHOTO LIGHTBOX (home mosaic)
(function() {
  const items = document.querySelectorAll('.mosaic-item');
  if (!items.length) return;
  const box = document.createElement('div');
  box.className = 'lightbox';
  box.innerHTML = '<button aria-label="Close">&times;</button><img alt=""><p></p>';
  document.body.appendChild(box);
  const img = box.querySelector('img'), cap = box.querySelector('p');
  const close = () => box.classList.remove('open');
  items.forEach(it => { it.tabIndex = 0; it.setAttribute('role', 'button'); });
  items.forEach(it => it.addEventListener('keydown', e => { if (e.key === 'Enter') it.click(); }));
  items.forEach(it => it.addEventListener('click', () => {
    const src = it.querySelector('img');
    if (!src) return; // placeholder only: nothing to enlarge
    img.src = src.src; cap.textContent = it.dataset.caption || '';
    box.classList.add('open');
  }));
  box.addEventListener('click', e => { if (e.target !== img) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
})();

// FORMS -> backend
(function() {
  const need = { prayer: 4, contact: 4, subscribe: 1 };
  const ok = { prayer: 'Thank you. Our prayer team will intercede for you! \uD83D\uDE4F', contact: "Message sent! We'll be in touch soon. God bless you! \uD83D\uDE4F", subscribe: 'Subscribed! God bless you! \uD83D\uDE4F' };
  const csrf = () => (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || '';
  document.querySelectorAll('[data-submit]').forEach(btn => btn.addEventListener('click', async () => {
    const kind = btn.dataset.submit;
    let box = btn.parentElement;
    while (box && box.querySelectorAll('input,select,textarea').length < need[kind]) box = box.parentElement;
    if (!box) return;
    const fields = [...box.querySelectorAll('input,select,textarea')].slice(0, need[kind]);
    btn.disabled = true;
    try {
      const r = await fetch('/api/' + kind + '/', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify({ fields: fields.map(f => f.value) }) });
      const d = await r.json();
      if (d.ok) { fields.forEach(f => { f.value = ''; }); alert(ok[kind]); } else alert(d.error || 'Something went wrong. Please try again.');
    } catch (e) { alert('Could not send. Please check your connection and try again.'); }
    btn.disabled = false;
  }));
})();
