import logging
from pathlib import Path
import re
log = logging.getLogger("mkdocs.plugins")
# Define the folders  to strip here directly
strip_folders = ['items', 'blocks', 'entities', 'passive', 'hostile','factions', 'misc', 'foods', 'utility', 'woods', 'stones', 'worldgen', 'world', 'biomes']

def on_pre_build(config):
    log.info(">>> Flatten Urls Porcessor: Present")

def on_files(files, config):
    for file in files:
        
        # Skip directories mistakenly detected as files
        if Path(file.abs_src_path).is_dir():
            print(f"[flatten-urls] Skipping directory: {file.abs_src_path}")
            continue

        # Skip non-markdown files
        if not file.src_path.endswith('.md'):
            continue

        parts = file.src_path.replace('\\', '/').split('/')
        # Filter out folders specified in strip_folders
        new_parts = [part for part in parts if part not in strip_folders]

        # If nothing changed, continue without modifying
        if parts == new_parts:
            continue
            
        # Rebuild the dest_path and url
        new_path = '/'.join(new_parts)

        # Set destination path to flattened structure with /index.html
        file.dest_path = new_path.replace('.md', '/index.html')

        # Set the URL to the flattened structure with trailing slash
        file.url = new_path.replace('.md', '/')

        #print(f"[flatten-urls] Rewriting {file.src_path} -> {file.dest_path} ({file.url})")

    return files