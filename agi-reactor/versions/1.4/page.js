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
    viewport.classList.toggle('is-zoomed', zoom > 1);
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
// Every expanded relationship figure has its own reversible zoom state.
(() => {
  document.querySelectorAll('.relationship-figure').forEach(figure => {
    const viewport = figure.querySelector('.figure-viewport');
    const svg = viewport.querySelector('svg');
    const output = figure.querySelector('output');
    let zoom = 1;
    function setZoom(next) {
      zoom = Math.max(1, Math.min(4, next));
      svg.style.width = `${zoom * 100}%`;
      viewport.classList.toggle('is-zoomed', zoom > 1);
      output.value = `${zoom * 100}%`;
      figure.querySelector('[data-zoom="out"]').disabled = zoom === 1;
      figure.querySelector('[data-zoom="in"]').disabled = zoom === 4;
      if (zoom === 1) viewport.scrollTo(0, 0);
    }
    figure.querySelectorAll('[data-zoom]').forEach(button => {
      button.addEventListener('click', () => setZoom(button.dataset.zoom === 'fit' ? 1 : zoom + (button.dataset.zoom === 'in' ? .5 : -.5)));
    });
    setZoom(1);
  });
})();
