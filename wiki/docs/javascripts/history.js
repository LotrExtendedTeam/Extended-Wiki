document.addEventListener('DOMContentLoaded', () => {
  const dropdown = document.querySelector('.edit-history-dropdown');
  const toggle = document.getElementById('edit-history-toggle');

  const viewBtn = document.getElementById('show-history-link');
  const modal = document.getElementById('history-modal');
  const closeBtn = document.querySelector('.close-btn');
  const list = document.getElementById('commit-list');
  const raw = document.getElementById('page-history');

  if (dropdown && toggle) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      dropdown.classList.toggle('show');
    });

    window.addEventListener('click', () => {
      dropdown.classList.remove('show');
    });
  }

  if (viewBtn && modal && raw && list) {
    viewBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const history = JSON.parse(raw.textContent);
      list.innerHTML = '';
      history.forEach(commit => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${commit.date}</strong> - ${commit.author}: ${commit.message} <code>(${commit.short})</code>`;
        list.appendChild(li);
      });
      modal.style.display = 'block';
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }

  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
});