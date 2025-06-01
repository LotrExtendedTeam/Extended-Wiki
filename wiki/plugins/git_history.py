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
            ['git', 'log', '--follow', '-n', '15', '--pretty=format:%h|%an|%ad|%s', '--date=short', '--', file_path],
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
            short, author, date, message = line.split('|', 3)
            history.append({
                'short': short,
                'author': author,
                'date': date,
                'message': message
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