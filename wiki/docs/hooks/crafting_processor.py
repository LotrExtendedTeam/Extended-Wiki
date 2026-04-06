import logging
import re
import json
from mkdocs.structure.pages import Page
import html

log = logging.getLogger("mkdocs.plugins")

CRAFTING_RE = re.compile(r"\{\{\s*crafting:(.*?)\s*\}\}", re.DOTALL)

# --- GLOBAL STORAGE ---
RECIPES = {}
ITEMS = {}
TAGS = {}
IMG_PATH = "/Extended-Wiki/wiki/img/"

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

def get_item(item_id):
    # Handle tags by taking first item
    if item_id.startswith("#"):
        tag_name = item_id[1:]
        items_in_tag = TAGS.get(tag_name, [])
        if items_in_tag:
            item_id = items_in_tag[0]
        else:
            return {
                "name": f"Missing tag: {tag_name}",
                "url": "#",
                "image": "missing.png"
            }

    return ITEMS.get(item_id, {
        "name": f"Missing: {item_id}",
        "url": "#",
        "image": "missing.png"
    })

# --- SLOT RENDER ---
def render_slot(item_id):
    if item_id is None:
        return '<div class="slot empty"></div>'

    item = get_item(item_id)
    return f'''
    <a href="{item["url"]}" 
       class="slot" 
       data-glightbox="skip" 
       data-name="{html.escape(item["name"])}">
        <img src="{IMG_PATH}{item["image"]}">
    </a>
    '''

# --- OUTPUT RENDER ---
def render_output(output):
    item = get_item(output["item"])
    count = output.get("count", 1)
    count_html = f'<span class="count">{count}</span>' if count > 1 else ""

    return f'''
    <a href="{item["url"]}" class="crafting-output slot" data-name="{item["name"]}">
        <img src="{IMG_PATH}{item["image"]}">
        {count_html}
    </a>
    '''

# --- INFO ---
def render_info(recipe):
    if recipe.get("type") == "shapeless":
        return "Shapeless"
    return "Shaped"

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
    info_html = render_info(recipe)

    html = ['<div class="crafting-box">']
    html.append(f'<div class="crafting-title">{recipe["title"]}</div>')
    html.append(f'<div class="crafting-body">')
    html.append(f'<div class="crafting-grid">')
    html.append(f'{grid_html}')
    html.append(f'</div>')
    html.append(f'{output_html}')
    html.append(f'<div class="crafting-info">')
    html.append(f'{info_html}')
    html.append(f'</div>')
    html.append(f'</div>')
    html.append(f'</div>')
    return '\n'.join(html)

# --- MARKDOWN HOOK ---
def on_page_markdown(markdown_content, page: Page, config, files):
    def render(match):
        recipe_id = match.group(1).strip()
        html = render_recipe(recipe_id)
        return render_recipe(recipe_id)

    new_markdown = CRAFTING_RE.sub(render, markdown_content)
    return new_markdown