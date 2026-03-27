import json
import subprocess
import logging
import os
from mkdocs.structure.pages import Page
log = logging.getLogger("mkdocs.plugins")

def on_pre_build(config):
    log.info(">>> Page Editor Injector: Present")

def on_page_markdown(markdown, page: Page, config, files):
    injected = f'''
<div id="editorModal" style="display:none;">
  <div id="editorBox">
    <div id="editorHeader">
      <span>Markdown Editor</span>
      <label style="margin-left:15px;">
        <input type="checkbox" id="editOwnFork"> Edit my fork directly
      </label>
      <button onclick="showDiff()">Preview Changes</button>
      <button onclick="submitEdit()">Submit</button>
      <button onclick="closeEditor()">Close</button>
    </div>

    <!-- PR Metadata -->
    <input id="prTitle" placeholder="PR Title" style="width:100%; margin:5px 0; padding:5px;" />
    <textarea id="prBody" placeholder="PR Description" style="width:100%; height:60px; padding:5px; margin-bottom:5px;"></textarea>

    <!-- Markdown Editor -->
    <textarea id="editor" style="width:100%; flex:1; padding:10px; font-family:monospace;"></textarea>

    <!-- Diff Viewer -->
    <div id="diffView" style="display:none; padding:10px; background:#1e1e1e; color:white; overflow:auto; height:150px; margin-top:5px;"></div>

    <!-- Progress Log -->
    <div id="progressLog" style="background:#111; color:#0f0; font-size:12px; padding:8px; height:120px; overflow-y:auto; margin-top:5px;"></div>
  </div>
</div>
'''

    return markdown + injected