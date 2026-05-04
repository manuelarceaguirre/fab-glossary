
const search = document.getElementById('search');
const rows = [...document.querySelectorAll('.nav-row')];
if (search) {
  search.addEventListener('input', () => {
    const q = search.value.trim().toLowerCase();
    rows.forEach((row) => {
      const text = row.textContent.toLowerCase();
      row.style.display = !q || text.includes(q) ? '' : 'none';
    });
  });
}
const links = [...document.querySelectorAll('.pager a')];
document.addEventListener('keydown', (event) => {
  if (event.target && ['INPUT', 'TEXTAREA'].includes(event.target.tagName)) return;
  if (event.key === 'ArrowLeft' && links[0]) location.href = links[0].href;
  if (event.key === 'ArrowRight' && links[1]) location.href = links[1].href;
  if (event.key === '/') { event.preventDefault(); search?.focus(); }
});
