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
IMG_PATH = "/images/items/"

# --- LOAD DATA ---
def on_pre_build(config):
    global RECIPES, ITEMS, TAGS
    log.info(">>> Crafting Processor: Loaded")

    with open("data/recipes.json") as f:
        RECIPES = json.load(f)

    with open("data/items.json") as f:
        ITEMS = json.load(f)
        
    with open("data/tags.json") as f:
        TAGS = json.load(f)

def format_name(name):
    return name.replace("_", " ").title()

def get_item(item_id):
    return ITEMS.get(item_id, {
        "name": f"Missing: {item_id}",
        "url": "#",
        "image": "missing.png"
    })

# --- SLOT RENDER ---
def render_slot(item_id):
    if item_id is None:
        return '<div class="slot empty"></div>'

    # TAG HANDLING
    if item_id.startswith("#"):
        tag_name = item_id[1:]
        tag_items = TAGS.get(tag_name, [])

        if not tag_items:
            return f'<div class="slot empty" title="Empty tag: {tag_name}"></div>'

        valid_items = [i for i in tag_items if i in ITEMS]
        if not valid_items:
            return f'<div class="slot empty" title="Invalid tag: {tag_name}"></div>'

        first_item = get_item(valid_items[0])
        items_data = ",".join(valid_items)

        return f'''
        <a href="/wiki/Tag:{format_name(tag_name)}"
           class="slot tag"
           data-name="Any {html.escape(format_name(tag_name))}"
           data-items="{items_data}">
            <img src="{IMG_PATH}{first_item["image"]}">
        </a>
        '''

    # NORMAL ITEM
    item = get_item(item_id)

    return f'''
    <a href="{item["url"]}" 
       class="slot" 
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
    <a href="{item["url"]}" 
       class="crafting-output slot" 
       data-name="{item["name"]}">
        <img src="{IMG_PATH}{item["image"]}">
        {count_html}
    </a>
    '''


# --- INFO ---
def render_info(recipe):
    if recipe.get("type") == "shapeless":
        return "Shapeless 🔄"
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

    return f"""
    <div class="crafting-box">
        <div class="crafting-title">{recipe["title"]}</div>

        <div class="crafting-body">

            <div class="crafting-grid">
                {grid_html}
            </div>

            {output_html}

            <div class="crafting-info">
                {info_html}
            </div>

        </div>
    </div>
    """


# --- MARKDOWN HOOK ---
def on_page_markdown(markdown_content, page: Page, config, files):
    def repl(match):
        recipe_id = match.group(1).strip()
        return render_recipe(recipe_id)

    return CRAFTING_RE.sub(repl, markdown_content)