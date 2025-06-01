document.addEventListener('DOMContentLoaded', () => {
  const dropdown = document.querySelector('.edit-history-dropdown');
  const toggle = document.getElementById('edit-history-toggle');

  if (dropdown && toggle) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      dropdown.classList.toggle('show');
    });

    window.addEventListener('click', () => {
      dropdown.classList.remove('show');
    });
  }
});