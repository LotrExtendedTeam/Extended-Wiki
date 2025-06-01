import json
import subprocess
import logging
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
log = logging.getLogger("mkdocs.plugins")

def on_pre_build(config):
    log.info(">>> Git History Injector: Present")

def on_page_markdown(markdown, page: Page, config, files):
    file_path = page.file.abs_src_path
    log.info(">>> Git History Injector: processing "+page.url+""+file_path)

    try:
        result = subprocess.run(
            ['git', 'log', '--follow', '-n', '15',
            '--pretty=format:%h|%H|%an|%ad|%at|%s', '--date=iso8601', '--', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        commits = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        return markdown

    history = []
    for line in commits:
        if '|' in line:
            short, full, author, date_str, timestamp, message = line.split('|', 5)
            # Get file stats
            stat = subprocess.run(
                ['git', 'show', '--stat', '--oneline', f'{full}', '--', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            added = removed = size = 'n/a'
            for stat_line in stat.stdout.splitlines():
                if file_path in stat_line and ('|' in stat_line):
                    parts = stat_line.strip().split('|')
                    if len(parts) >= 2:
                        stat_info = parts[1].strip()
                        added = stat_info.count('+')
                        removed = stat_info.count('-')
            try:
                size_bytes = os.path.getsize(file_path)
            except:
                size_bytes = 0
            history.append({
                'short': short,
                'full': full,
                'author': author,
                'date': date_str,
                'timestamp': int(timestamp),
                'message': message,
                'added': added,
                'removed': removed,
                'size': size_bytes
            })

    history_json = json.dumps(history)

    injected = f'''
<div id="history-modal" style="display:none;">
  <div class="modal-content">
    <span class="close-btn">&times;</span>
    <h3>Edit History</h3>
    <ul id="commit-list"></ul>
  </div>
</div>
<script id="page-history" type="application/json">{history_json}</script>
'''

    return markdown + injected