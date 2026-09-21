'use strict';
const category = document.getElementById('category');
if (category) {
  const family = document.getElementById('family');
  const view = document.getElementById('view');
  const search = document.getElementById('search');
  const rows = [...document.querySelectorAll('.experiment')];
  function filter() {
    let count = 0;
    const query = search.value.trim().toLocaleLowerCase();
    for (const row of rows) {
      const matchCategory = category.value === 'all' || (category.value === 'current' ? row.dataset.category !== 'history' : row.dataset.category === category.value);
      const visible = matchCategory && (family.value === 'all' || row.dataset.family === family.value) && (view.value === 'all' || row.dataset.views.split(' ').includes(view.value)) && row.dataset.search.toLocaleLowerCase().includes(query);
      row.hidden = !visible;
      count += Number(visible);
    }
    document.getElementById('count').textContent = `显示 ${count} / ${rows.length} 项实验`;
    document.getElementById('empty').hidden = count !== 0;
  }
  for (const input of [category, family, view, search]) input.addEventListener('input', filter);
  document.getElementById('clear').addEventListener('click', () => {
    category.value = 'current'; family.value = 'all'; view.value = 'all'; search.value = ''; filter();
  });
  filter();
}
