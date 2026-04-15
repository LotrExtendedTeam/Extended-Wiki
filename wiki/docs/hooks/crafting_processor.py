import logging
import re
import os
import json
from mkdocs.structure.pages import Page
import html
import imageio.v2 as imageio
from PIL import Image
import numpy as np

log = logging.getLogger("mkdocs.plugins")

CRAFTING_RE = re.compile(r"\{\{\s*crafting:(.*?)\s*\}\}", re.DOTALL)
CRAFTING_GRID_RE = re.compile(r"\{\{\s*craftinggrid:(.*?)\s*\}\}", re.DOTALL)

# --- GLOBAL STORAGE ---
RECIPES = {}
ITEMS = {}
TAGS = {}
URL_PATH = "/Extended-Wiki/wiki/img/"
checked_images = set()

# --- LOAD DATA ---
def on_pre_build(config):
    global RECIPES, ITEMS, TAGS
    log.info(">>> Crafting Processor: Loading data")

    try:
        with open("wiki/docs/hooks/craftingoutput/recipes.json") as f:
            RECIPES = json.load(f)
    except Exception as e:
        log.warning(f"Failed to load recipes.json: {e}")
        RECIPES = {}

    try:
        with open("wiki/docs/hooks/craftingoutput/items.json") as f:
            ITEMS = json.load(f)
    except Exception as e:
        log.warning(f"Failed to load items.json: {e}")
        ITEMS = {}

    try:
        with open("wiki/docs/hooks/craftingoutput/tags.json") as f:
            TAGS = json.load(f)
    except Exception as e:
        log.warning(f"Failed to load tags.json: {e}")
        TAGS = {}

    # Generate tag GIFs
    for tag_id, tag_data in TAGS.items():
        gif_path = generate_tag_gif(tag_id, tag_data, ITEMS)
        # Store it back into tag data
        if gif_path:
            tag_data["image"] = gif_path

def get_item(item_id):
    # Handle tags
    if item_id.startswith("#"):
        tag_name = item_id[1:]
        tag_data = TAGS.get(tag_name)
        if tag_data:
            if "image" in tag_data and tag_data["image"].endswith(".gif"):
                return {
                    "name": tag_data.get("name", f"Tag: {tag_name}"),
                    "url": tag_data.get("url", "#"),
                    "image": tag_data["image"]
                }
            return {
                "name": tag_data.get("name", f"Tag: {tag_name}"),
                "url": tag_data.get("url", "#"),
                "image": URL_PATH + "unknown.png"
            }
        return {
            "name": f"Missing tag: {tag_name}",
            "url": "#",
            "image": URL_PATH + "unknown.png"
        }
    # Normal item
    return ITEMS.get(item_id, {
        "name": f"Missing: {item_id}",
        "url": "#",
        "image": "unknown.png"
    })

def generate_tag_gif(tag_id, tag_data, items_data):
    base_frame_dir = "wiki/docs/wiki/img/"
    output_rel = f"tags/{tag_id.replace(':', '_').replace('/', '_')}.gif"
    output_abs = os.path.join("wiki/docs/wiki/img/generated/", output_rel)
    os.makedirs(os.path.dirname(output_abs), exist_ok=True)
    # Skip if no items
    item_ids = tag_data.get("items", [])
    if not item_ids:
        return None
    # Build frame paths from item images
    frame_paths = []
    for item_id in item_ids:
        item = items_data.get(item_id)
        if not item:
            continue
        image_path = item.get("image")
        if not image_path:
            continue
        full_path = getImageLocal(image_path)
        frame_paths.append(full_path)
    if not frame_paths:
        return None
    # Generate GIF
    print(f"[TAG GIF] Generating: {output_rel}")
    TARGET_SIZE = (16, 16)
    frames = []
    for f in frame_paths:
        try:
            img = Image.open(f).convert("RGBA")
            img = img.resize(TARGET_SIZE, Image.NEAREST)
            arr = np.array(img)
            # Safety check
            if arr.shape != (16, 16, 4):
                log.warning(f"[TAG GIF] Skipping bad shape: {f} {arr.shape}")
                continue
            frames.append(arr)
        except Exception as e:
            log.warning(f"[TAG GIF] Failed reading frame {f}: {e}")
        #images = [imageio.imread(f) for f in frame_paths[:16]]  # limit frames (optional)
    imageio.mimsave(output_abs, frames, format="GIF", duration=1000, loop=0)

    return f"generated/{output_rel}"

def getImageLocal(imagePath):
    base = "wiki/docs/wiki/img/"
    if not imagePath:
        return os.path.join(base, "unknown.png")
    local_path = os.path.join(base, imagePath)
    # Only check once per image
    if imagePath not in checked_images:
        checked_images.add(imagePath)
        if not os.path.exists(local_path):
            log.warning(f"Missing image: {imagePath}")
            return os.path.join(base, "unknown.png")
    if os.path.exists(local_path):
        return local_path
    else:
        return os.path.join(base, "unknown.png")

def getImage(imagePath):
    if not imagePath:
        return URL_PATH + "unknown.png"
    local_path = os.path.join("wiki/docs/wiki/img/", imagePath)
    # Only check once per image
    if imagePath not in checked_images:
        checked_images.add(imagePath)
        if not os.path.exists(local_path):
            log.warning(f"Missing image: {imagePath}")
            return URL_PATH + "unknown.png"
    if os.path.exists(local_path):
        return URL_PATH + imagePath
    else:
        return URL_PATH + "unknown.png"

def fix_url(url):
    if url=="#":
        return "/Extended-Wiki/404"
    return url
        
# --- SLOT RENDER ---
def render_slot(item_id):
    if item_id is None:
        return '<div class="crafting-slot empty"></div>'

    item = get_item(item_id)
    display_name = item.get("tooltip") or item["name"]
    return f'''
    <a href="{fix_url(item["url"])}" class="crafting-slot" data-name="{html.escape(display_name)}">
        <img src="{getImage(item["image"])}" class="off-glb" loading="lazy">
    </a>
    '''

# --- OUTPUT RENDER ---
def render_output(output):
    item = get_item(output["item"])
    count = output.get("count", 1)
    count_html = f'<span class="count">{count}</span>' if count > 1 else ""
    display_name = item.get("tooltip") or item["name"]
    return f'''
    <a href="{fix_url(item["url"])}" class="crafting-output crafting-slot" data-name="{html.escape(display_name)}">
        <img src="{getImage(item["image"])}" class="off-glb" loading="lazy">
        {count_html}
    </a>
    '''

# --- INFO ---
def render_gui_img(recipe):
    if recipe.get("type") == "shapeless":
        grid_image = "crafting_grid_shapeless.png"
    else:
        grid_image = "crafting_grid.png"
    return grid_image

LOWERCASE_KEYS = {"collapsible"}

def parse_grid_input(content):
    parts = content.split(";")
    options = {}
    recipes_part = ""

    if len(parts) > 1:
        # first part = options
        for opt in parts[0].split(","):
            if "=" in opt:
                k, v = opt.split("=", 1)
                key = k.strip()
                value = v.strip()
                if key in LOWERCASE_KEYS:
                    value = value.lower()
                options[key] = value
        recipes_part = parts[1]
    else:
        recipes_part = parts[0]

    recipe_ids = [r.strip() for r in recipes_part.split(",") if r.strip()]
    return options, recipe_ids

def render_crafting_grid(content):
    options, recipe_ids = parse_grid_input(content)
    collapsible = options.get("collapsible") == "true"

    rows_html = []
    for i in range(0, len(recipe_ids), 2):  # group every 2
        pair = recipe_ids[i:i+2]
        pair_html = ''.join(render_recipe(r) for r in pair)
        rows_html.append(f'<div class="crafting-row">{pair_html}</div>')
    
    crafting_html = ['<div class="crafting-grid-layout">']
    crafting_html.append(''.join(rows_html))
    crafting_html.append(f'</div>')
    finalHTML ='\n'.join(crafting_html)
    
    if collapsible:
        return render_collapsible_grid(finalHTML, options)
    else:
        return finalHTML

def render_collapsible_grid(inner_html, options):
    title = options.get("title", "Crafting Recipes")
    default_open = options.get("open") == "true"
    display = "block" if default_open else "none"
    label = "Collapse" if default_open else "Expand"
    html_output = []

    html_output.append('<div class="crafting-collapsible">')
    # Header
    html_output.append('<div class="crafting-collapsible-header">')
    html_output.append(f'<span class="crafting-collapsible-title">{html.escape(title)}</span>')
    html_output.append(f'<button class="crafting-toggle-btn" onclick="toggleCrafting(this)">[<span class="toggle-text">{label}</span>]</button>')
    html_output.append('</div>')  # end header
    # Content
    html_output.append(f'<div class="crafting-collapsible-content" style="display: {display};">')
    html_output.append(f'<div class="crafting-grid-layout">{inner_html}</div>')
    html_output.append('</div>')  # collapsible-content

    html_output.append('</div>')  # collapsible root
    return '\n'.join(html_output)

# --- MAIN RENDER ---
def render_recipe(recipe_id):
    recipe = RECIPES.get(recipe_id)

    if not recipe:
        return f"<b>Unknown recipe: {recipe_id}</b>"

    grid_html = "".join(
        render_slot(item)
        for row in recipe["grid"]
        for item in row
    )

    output_html = render_output(recipe["output"])
    grid_image = render_gui_img(recipe)

    html = ['<div class="crafting-box">']
    html.append(f'<div class="crafting-body">')
    html.append(f'<img class="crafting-gui off-glb" src="/Extended-Wiki/wiki/img/gui/{grid_image}" alt="Crafting GUI">')
    html.append(f'<div class="crafting-title-overlay">{recipe["title"]}</div>')
    html.append(f'<div class="crafting-grid">{grid_html}</div>')
    html.append(f'{output_html}')
    #html.append(f'<div class="crafting-info">{info_html}</div>')
    html.append(f'</div>')
    html.append(f'</div>')
    return '\n'.join(html)

# --- MARKDOWN HOOK ---
def on_page_markdown(markdown_content, page: Page, config, files):
    def render_grid(match):
        content = match.group(1)
        return render_crafting_grid(content)

    def render_single(match):
        recipe_id = match.group(1).strip()
        return render_recipe(recipe_id)

    # IMPORTANT: process grid first
    markdown_content = CRAFTING_GRID_RE.sub(render_grid, markdown_content)

    # then individual crafting blocks
    markdown_content = CRAFTING_RE.sub(render_single, markdown_content)
    return markdown_content