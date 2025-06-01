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
        // Format date
        const date = new Date(commit.timestamp * 1000);
        const formattedDate = date.toLocaleString('en-GB', {
          day: '2-digit', month: 'long', year: 'numeric',
          hour: '2-digit', minute: '2-digit', hour12: false
        });
        const commitLink = `https://github.com/LotrExtendedTeam/Extended-Wiki/commit/${commit.full}`;
        const authorLink = `https://github.com/${commit.author}`;
        const sizeFormatted = commit.size.toLocaleString();
        const netChange = commit.change;
        const changeClass = netChange > 0 ? 'commit-change-positive'
                  : netChange < 0 ? 'commit-change-negative'
                  : 'commit-change-neutral';
        const changeText = netChange > 0 ? `+${netChange.toLocaleString()}`
                  : netChange < 0 ? `-${netChange.toLocaleString()}`
                  : netChange.toLocaleString();

        li.innerHTML = `
          <code><a href="${commitLink}" target="_blank">(${commit.short})</a></code>
          ${formattedDate}
          <a href="${authorLink}" target="_blank">${commit.author}</a>
          ... (${sizeFormatted} bytes)
          <span class="${changeClass}">(${changeText})</span>
          <em>(${commit.message})</em>
        `;
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