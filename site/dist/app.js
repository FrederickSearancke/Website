const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
});
nav?.addEventListener('click', event => {
  if (event.target.closest('a')) { nav.classList.remove('open'); toggle?.setAttribute('aria-expanded', 'false'); }
});
document.addEventListener('keydown', event => {
  if(event.key === 'Escape' && nav?.classList.contains('open')) { nav.classList.remove('open'); toggle?.setAttribute('aria-expanded','false'); toggle?.focus(); }
});
const filters = [...document.querySelectorAll('[data-filter]')];
const projectRows = [...document.querySelectorAll('[data-category]')];
filters.forEach(button => button.addEventListener('click', () => {
  const category = button.dataset.filter;
  filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  let count = 0;
  projectRows.forEach(row => { row.hidden = category !== 'all' && row.dataset.category !== category; if(!row.hidden) count++; });
  const status = document.getElementById('filter-status');
  if(status) status.textContent = `${count} project${count === 1 ? '' : 's'} shown`;
}));


// Native dialog supplies keyboard dismissal, focus containment, and a modal backdrop.
const visualInspector = document.getElementById('visual-inspector');
const visualTrigger = document.querySelector('[data-open-visual]');
if (visualInspector && visualTrigger && typeof visualInspector.showModal === 'function') {
  visualTrigger.addEventListener('click', event => {
    event.preventDefault();
    visualInspector.showModal();
    document.body.classList.add('visual-inspector-open');
  });
  visualInspector.addEventListener('close', () => {
    document.body.classList.remove('visual-inspector-open');
    visualTrigger.focus({ preventScroll: true });
  });
  // Clear the overlay before following the chapter link, including back/forward restoration.
  visualInspector.querySelector('.visual-chapter-link')?.addEventListener('click', () => visualInspector.close());
  window.addEventListener('pagehide', () => {
    if (visualInspector.open) visualInspector.close();
    document.body.classList.remove('visual-inspector-open');
  });
}

// Finish a direct chapter jump once font metrics are final. Image space is
// reserved in the HTML; do not interrupt someone who has already started reading.
const projectionHeading = document.getElementById('vector-projection');
if (projectionHeading) {
  let cancelPendingAlignment = () => {};
  const alignProjectionHeading = () => {
    cancelPendingAlignment();
    if (location.hash !== '#vector-projection') return;

    const pending = new AbortController();
    cancelPendingAlignment = () => pending.abort();
    for (const event of ['wheel', 'touchstart', 'pointerdown', 'keydown']) {
      window.addEventListener(event, cancelPendingAlignment, { passive: true, signal: pending.signal });
    }
    Promise.resolve(document.fonts?.ready).then(() => {
      requestAnimationFrame(() => {
        if (!pending.signal.aborted && location.hash === '#vector-projection') {
          projectionHeading.scrollIntoView({ block: 'start', behavior: 'instant' });
        }
        pending.abort();
      });
    });
  };
  alignProjectionHeading();
  window.addEventListener('hashchange', alignProjectionHeading);
  window.addEventListener('pagehide', () => cancelPendingAlignment());
}
