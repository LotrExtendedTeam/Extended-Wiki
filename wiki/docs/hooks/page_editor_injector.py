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
<div id="edit-modal-overlay" class="edit-modal-overlay" onclick="closeSelection(event)">
  
  <div class="edit-modal" onclick="event.stopPropagation()">
    
    <button class="edit-modal-close" onclick="closeSelection()">&times;</button>

    <div class="edit-modal-header">
      <h2 class="edit-modal-title">Choose Editing Method</h2>
    </div>

    <div class="edit-modal-divider"></div>

    <div class="edit-modal-actions">
      
      <a id="edit-github" class="md-button md-button--primary" target="_blank" data-md-component="button">
        Edit on GitHub
      </a>

      <a id="edit-anon" class="md-button" data-md-component="button">
        Edit Anonymously
      </a>

      <a id="edit-token" class="md-button" data-md-component="button">
        Edit with Token
      </a>

      <div id="pat-token-container" style="display:none; flex-direction: column; gap:0.5rem;">
        <input 
          type="password" 
          id="pat-token-input" 
          placeholder="Enter GitHub PAT..." 
          class="md-input"
          style="padding:0.5rem; border-radius:8px; border:1px solid var(--md-default-table-content-border-color);"
        />
        <div style="display:flex; gap:0.5rem;">
          <button id="save-pat" class="md-button md-button--primary">Save Token</button>
          <button id="clear-pat" class="md-button">Clear Token</button>
        </div>
      </div>
    </div>

  </div>
</div>
'''

    return markdown + injected