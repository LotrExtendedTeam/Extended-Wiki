import logging
from pathlib import Path
import re
log = logging.getLogger("mkdocs.plugins")

#Configuration
PARENT_FOLDER = "wiki"  # The root folder under which subfolders will be flattened
EXCLUDE_FOLDERS = {"keep_this", "archive"}  # Folders to keep intact (using a set for O(1) lookups)

def on_pre_build(config):
    log.info(">>> Flatten Urls Processor: Present")

def on_files(files, config):
    for file in files:
        
        # Skip directories and non-markdown files
        if Path(file.abs_src_path).is_dir() or not file.src_path.endswith('.md'):
            continue

        path_parts = list(Path(file.src_path).parts)

        # Check if the file is inside the target parent folder
        if PARENT_FOLDER in path_parts:
            parent_idx = path_parts.index(PARENT_FOLDER)
            
            # Extract parts: prefix before parent, the parent itself, and remaining target parts
            prefix = path_parts[:parent_idx + 1]
            target_parts = path_parts[parent_idx + 1:]

            # Retain only the filename and any directory present in EXCLUDE_FOLDERS
            filtered_parts = [
                part for part in target_parts[:-1] if part in EXCLUDE_FOLDERS
            ] + [target_parts[-1]]

            new_parts = prefix + filtered_parts

            # If the path structure was modified, update destination and URL properties
            if new_parts != path_parts:
                new_path = '/'.join(new_parts)

                # Update MkDocs File attributes
                file.dest_path = new_path.replace('.md', '/index.html')
                file.url = new_path.replace('.md', '/')
    return files
