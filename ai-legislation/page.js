(() => {
  const input = document.querySelector('#state-search');
  const select = document.querySelector('#pathway-filter');
  const records = [...document.querySelectorAll('.state-record')];
  const count = document.querySelector('#ledger-count');
  const empty = document.querySelector('.filter-empty');
  const filter = () => {
    const query = input.value.trim().toLocaleLowerCase();
    let shown = 0;
    records.forEach(record => {
      record.hidden = !(record.textContent.toLocaleLowerCase().includes(query) && (select.value === 'all' || record.dataset.pathway === select.value));
      if (!record.hidden) shown++;
    });
    count.textContent = `${shown} jurisdiction${shown === 1 ? '' : 's'}`;
    empty.hidden = shown !== 0;
  };
  input.addEventListener('input', filter);
  select.addEventListener('change', filter);
  document.querySelector('.ledger-filter').addEventListener('reset', () => requestAnimationFrame(filter));
  // A citation always reveals its target, even if a prior search hid the state.
  const revealTarget = () => {
    const id = location.hash.slice(1);
    if (!id.startsWith('state-')) return;
    const target = document.getElementById(id);
    if (target && target.hidden) {
      input.value = ''; select.value = 'all'; filter();
      requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
    }
  };
  window.addEventListener('hashchange', revealTarget);
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#state-"]');
    if (link) {
      const target = document.getElementById(link.hash.slice(1));
      if (target?.hidden) { input.value=''; select.value='all'; filter(); }
    }
  });
  revealTarget();
})();
