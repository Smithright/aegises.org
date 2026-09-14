(() => {
  const viewport = document.getElementById('map-viewport');
  const diagram = viewport.querySelector('svg');
  const label = document.getElementById('zoom-label');
  const plus = document.getElementById('zoom-in');
  const minus = document.getElementById('zoom-out');
  let zoom = 1;
  function setZoom(next) {
    const previous = zoom;
    const centerX = (viewport.scrollLeft + viewport.clientWidth / 2) / previous;
    const centerY = (viewport.scrollTop + viewport.clientHeight / 2) / previous;
    zoom = Math.min(4, Math.max(1, next));
    diagram.style.width = `${zoom * 100}%`;
    label.value = `${Math.round(zoom * 100)}%`;
    viewport.scrollLeft = centerX * zoom - viewport.clientWidth / 2;
    viewport.scrollTop = centerY * zoom - viewport.clientHeight / 2;
    plus.disabled = zoom >= 4;
    minus.disabled = zoom <= 1;
  }
  plus.addEventListener('click', () => setZoom(zoom + .5));
  minus.addEventListener('click', () => setZoom(zoom - .5));
  document.getElementById('zoom-reset').addEventListener('click', () => {setZoom(1); viewport.scrollTo(0,0);});
  setZoom(1);
  // All substantive text is in the initial HTML. Printing expands the technical appendix.
  let openBeforePrint = [];
  window.addEventListener('beforeprint', () => {
    openBeforePrint = [...document.querySelectorAll('details')].map(d => [d,d.open]);
    document.querySelectorAll('.full-spec').forEach(d => d.open = true);
  });
  window.addEventListener('afterprint', () => openBeforePrint.forEach(([d,open]) => d.open = open));
})();
