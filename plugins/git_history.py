import json
import subprocess
import logging
import os
from mkdocs.structure.pages import Page
log = logging.getLogger("mkdocs.plugins")

def on_pre_build(config):
    log.info(">>> Git History Injector: Present")

def get_commit_file_paths(start_path, repo_root):
    cmd = ['git', 'log', '--follow', '--name-status', '--pretty=format:%H', '--', start_path]
    result = subprocess.run(cmd, cwd=repo_root, stdout=subprocess.PIPE, text=True, check=True)
    lines = result.stdout.strip().split('\n')

    commit_paths = {}
    current_commit = None
    current_path = start_path

    for line in lines:
        if len(line) == 40 and all(c in '0123456789abcdef' for c in line):  # commit hash
            current_commit = line
            commit_paths[current_commit] = current_path
        elif line.startswith('R'):  # rename line, e.g. "R100\told_path\tnew_path"
            parts = line.split('\t')
            if len(parts) == 3:
                _, old_path, new_path = parts
                current_path = old_path  # File path *before* this commit was the old path

    return commit_paths

def on_page_markdown(markdown, page: Page, config, files):
    file_path = page.file.abs_src_path

    try:
        result = subprocess.run(
            ['git', 'log', '--follow', '-n', '50',
            '--pretty=format:%h|%H|%an|%ad|%at|%s', '--date=iso8601', '--', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        commits = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        return markdown

    # Get relative path from repo root
    repo_root = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    ).stdout.strip()
    # Get commit relative path currently
    rel_path = os.path.relpath(file_path, repo_root).replace('\\', '/')
    # Get commit relative path history
    commit_path_map = get_commit_file_paths(rel_path, repo_root)
    
    history = []
    
    # commits are newest to oldest, reverse to oldest first:
    commits = commits[::-1]
    
    previous_size = 0
    for line in commits:
        if '|' in line:
            short, full, author, date_str, timestamp, message = line.split('|', 5)

            # Get commit relative path to commit history
            commit_file_path = commit_path_map.get(full, rel_path)
            # Get commit file size
            size_result = subprocess.run(
                ['git', 'cat-file', '-s', f'{full}:{commit_file_path}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                size_bytes = int(size_result.stdout.strip())
            except ValueError:
                size_bytes = 0
            # calculate file size change
            net_change = size_bytes - previous_size
            previous_size = size_bytes
            # Cap message history at 50 chars
            message = (message.strip()[:47] + "...") if len(message.strip()) > 50 else message.strip()
            # Store indexed data
            history.append({
                'short': short,
                'full': full,
                'author': author,
                'date': date_str,
                'timestamp': int(timestamp),
                'message': message,
                'change': net_change,
                'size': size_bytes
            })
    # Reverse history since it was generated backwards
    history = history[::-1]
    # Convert to json
    history_json = json.dumps(history)
    # Build html to inject into page
    injected = f'''
<div id="history-modal" style="display:none;">
  <div id="history-modal-wrapper">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Edit History</h3>
        <span class="close-btn">&times;</span>
      </div>
      <ul id="commit-list"></ul>
    </div>
  </div>
</div>
<script id="page-history" type="application/json">{history_json}</script>
'''

    return markdown + injected