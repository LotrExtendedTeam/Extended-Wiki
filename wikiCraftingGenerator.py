import json
import os
import logging
log = logging.getLogger("recipe_generator")
logging.basicConfig(level=logging.INFO)

# --- TAG PATHS ---
TAG_FOLDERS = [
    "wikiDataGen/extended/data/forge/tags/items",
    "wikiDataGen/extended/data/lotr/tags/items",
    "wikiDataGen/extended/data/lotrextended/tags/items",
    "wikiDataGen/extended/data/minecraft/tags/items",
    "wikiDataGen/vanilla/data/forge/tags/items",
    "wikiDataGen/vanilla/data/minecraft/tags/items",
    "wikiDataGen/renewed/data/forge/tags/items",
    "wikiDataGen/renewed/data/lotr/tags/items",
    "wikiDataGen/renewed/data/minecraft/tags/items",
]

# --- RECIPE PATHS ---
LOTR_RECIPES = "wikiDataGen/renewed/recipes"
EXTENDED_RECIPES = "wikiDataGen/extended/recipes"

# --- OUTPUT PATHS ---
OUTPUT_FOLDER = "wiki/docs/hooks/craftingoutput"
OUTPUT_RECIPES_FILE = OUTPUT_FOLDER+"/recipes.json"
OUTPUT_TAGS_FILE = OUTPUT_FOLDER+"/tags.json"
OUTPUT_ITEMS_FILE = OUTPUT_FOLDER+"/items.json"

# --- MANUAL TAG OVERRIDES ---
# e.g. {"minecraft:planks": "minecraft:oak_plank"} will replace #minecraft:planks with minecraft:oak_plank
# Sometimes tags are only used for modpack compatability but for our purposes they can be simplified to a single item
# --- MANUAL TAG OVERRIDES ---
TAG_REPLACEMENTS = {
    # "tag_name": "item_id"
    # example: "planks": "oak_plank"
    "forge:nuggets/iron": "minecraft:iron_nugget",
    "forge:nuggets/silver": "lotr:silver_nugget",
    "forge:nuggets/gold": "minecraft:gold_nugget",
    "forge:nuggets/orc_steel": "lotr:orc_steel_nugget",
    "forge:ingots/bronze": "lotr:bronze_ingot",
    "forge:ingots/uruk_steel": "lotr:uruk_steel_ingot",
    "forge:ingots/orc_steel": "lotr:orc_steel_ingot",
    "forge:ingots/dwarven_steel": "lotr:dwarven_steel_ingot",
    "forge:ingots/elven_steel": "lotr:elven_steel_ingot",
    "forge:ingots/morgul_steel": "lotr:morgul_steel_ingot",
    "forge:ingots/iron": "minecraft:iron_ingot",
    "forge:dyes/yellow": "minecraft:yellow_dye",
    "forge:dyes/green": "minecraft:green_dye",
    "forge:dyes/red": "minecraft:yellow_dye",
    "forge:dyes/white": "minecraft:white_dye",
    "forge:dyes/blue": "minecraft:blue_dye",
    "forge:string": "minecraft:string",
}

# --- UTILITIES ---
def empty_grid():
    return [[None for _ in range(3)] for _ in range(3)]

# --- TAG HANDLING ---
def merge_tag_folders(folders):
    """
    Recursively load all tags from the given folders and subfolders.
    Each JSON file becomes a tag. Nested folders become subpaths.
    The namespace is inferred from the folder structure (e.g., data/<namespace>/...).
    """
    tags = {}
    for base_folder in folders:
        if not os.path.exists(base_folder):
            continue

        log.info(f"Loading from tag '{base_folder}'")
        # Determine namespace from path
        parts = os.path.normpath(base_folder).split(os.sep)
        try:
            ns_index = parts.index("data") + 1
            namespace = parts[ns_index]
        except Exception:
            namespace = "unknown"

        for root, _, files in os.walk(base_folder):
            for file in files:
                if not file.endswith(".json"):
                    continue
                full_path = os.path.join(root, file)

                # Relative path from base_folder
                rel_path = os.path.relpath(full_path, base_folder)
                tag_path = os.path.splitext(rel_path)[0].replace("\\", "/")  # normalize

                # Namespaced tag name
                tag_name = f"{namespace}:{tag_path}"

                try:
                    with open(full_path) as f:
                        data = json.load(f)
                        values = data.get("values", [])
                    #log.info(f"Loaded tag '{tag_name}' with {len(values)} values")
                except Exception as e:
                    log.warning(f"Failed to load tag {tag_name}: {e}")
                    values = []

                if tag_name in tags:
                    tags[tag_name].extend(values)
                else:
                    tags[tag_name] = values

    # Deduplicate
    for k in tags:
        tags[k] = list(dict.fromkeys(tags[k]))
    return tags

def resolve_tag(tag_name, all_tags, seen=None):
    """
    Recursively resolve a tag into a flat list of item IDs.
    Logs warnings for missing subtags.
    """
    if seen is None:
        seen = set()

    if tag_name in seen:
        log.warning(f"Circular reference detected for tag '{tag_name}'")
        return []

    seen.add(tag_name)

    if tag_name not in all_tags:
        log.warning(f"Tag '{tag_name}' not found")
        return []

    resolved = []
    for val in all_tags[tag_name]:
        val = val.strip()
        if val.startswith("#"):
            subtag_name = val[1:]
            #log.info(f"Resolving tag '{val}'")
            resolved.extend(resolve_tag(subtag_name, all_tags, seen))
        else:
            resolved.append(val)

    # Deduplicate
    return list(dict.fromkeys(resolved))

def flatten_tags(all_tags):
    """
    Returns a dict of tags -> only items (subtags fully resolved).
    Tags that resolve to no items are omitted.
    """
    flat_tags = {}
    for tag_name in all_tags:
        items = resolve_tag(tag_name, all_tags)
        if items:
            flat_tags[tag_name] = items
            #log.info(f"Tag '{tag_name}' resolved to {len(items)} items")
        else:
            log.warning(f"Tag '{tag_name}' has no resolved items and will be skipped")
    return flat_tags
    
# --- RECIPE VALIDATION ---
def validate_ingredient(ingredient, all_items, tags):
    if ingredient is None:
        return True
    if ingredient.startswith("#"):
        tag_name = ingredient[1:]
        resolved = tags.get(tag_name, [])
        if not resolved:
            log.warning(f"Recipe ingredient tag '{tag_name}' has no resolved items")
        return tag_name in tags and len(resolved) > 0
    else:
        if ingredient not in all_items:
            log.warning(f"Recipe ingredient '{ingredient}' does not exist in items")
        return ingredient in all_items

def validate_recipe(recipe, all_items, tags, recipe_id):
    valid = True
    for y, row in enumerate(recipe["grid"]):
        for x, ing in enumerate(row):
            if ing and not validate_ingredient(ing, all_items, tags):
                log.warning(f"Invalid ingredient '{ing}' in recipe '{recipe_id}' at position [{y},{x}]")
                valid = False
    return valid

def filter_unused_tags(tags, recipes):
    used_tags = set()
    for r in recipes.values():
        for row in r["grid"]:
            for ing in row:
                if ing and ing.startswith("#"):
                    used_tags.add(ing[1:])

    filtered = {}
    for t in used_tags:
        resolved_items = tags.get(t, [])
        if resolved_items:
            filtered[t] = resolved_items
        else:
            log.info(f"Tag '{t}' is used in recipes but resolves to nothing, skipping")
    return filtered

# --- GRID ALIGNMENT ---
def align_pattern_bottom_right(pattern_grid):
    rows = len(pattern_grid)
    cols = max(len(r) for r in pattern_grid)
    grid = [[None]*3 for _ in range(3)]
    start_row = 3 - rows
    start_col = 3 - cols
    for y, row in enumerate(pattern_grid):
        for x, val in enumerate(row):
            grid[start_row + y][start_col + x] = val
    return grid

# --- INGREDIENT PARSING ---
def parse_ingredient(ingredient):
    if ingredient is None:
        return None
    if isinstance(ingredient, list):
        ingredient = ingredient[0]
    if "item" in ingredient:
        return ingredient["item"]
    if "tag" in ingredient:
        tag_name = ingredient["tag"]
        # Apply replacement if needed
        if tag_name in TAG_REPLACEMENTS:
            return TAG_REPLACEMENTS[tag_name]
        return "#" + tag_name  # e.g. "#forge:rods/wooden"
    return None

def parse_shaped(data):
    raw_pattern = data.get("pattern", [])
    key = data.get("key", {})
    pattern_grid = []
    for row in raw_pattern:
        row_list = []
        for char in row:
            if char == " ":
                row_list.append(None)
            else:
                row_list.append(parse_ingredient(key.get(char)))
        pattern_grid.append(row_list)
    return align_pattern_bottom_right(pattern_grid)

def parse_shapeless(data):
    grid = empty_grid()
    ingredients = data.get("ingredients", [])
    for i, ing in enumerate(ingredients[:9]):
        x = i % 3
        y = i // 3
        grid[y][x] = parse_ingredient(ing)
    return grid

def parse_result(data):
    result = data.get("result")
    if isinstance(result, dict):
        return {"item": result["item"], "count": result.get("count", 1)}
    return {"item": result, "count": 1}

def normalize_recipe_type(rtype):
    if rtype in ["minecraft:shaped", "lotr:faction_shaped"]:
        return "shaped"
    elif rtype in ["minecraft:shapeless", "lotr:faction_shapeless"]:
        return "shapeless"
    return None

def get_recipe_title(rtype, table, output_item):
    if rtype.startswith("lotr:faction_") and table:
        return table.split(":")[-1].replace("_", " ").title() + " Crafting"
    else:
        return "Crafting"

def format_item_name(item_id):
    # Remove namespace and convert snake_case to Title Case
    name = item_id.split(":")[-1].replace("_", " ").title()
    return name

def format_item_url(item_id):
    namespace, name = item_id.split(":")
    if namespace == "minecraft":
        words = name.replace("-", "_").split("_")
        formatted_name = "_".join(word.capitalize() for word in words)
        return f"https://minecraft.wiki/w/{formatted_name}"
    elif namespace == "lotr":
        # LOTR wiki uses underscores instead of spaces
        words = name.replace("-", "_").split("_")
        formatted_name = "_".join(word.capitalize() for word in words)
        #return f"https://lotrextendedteam.github.io/Extended-Wiki/wiki/{formatted_name}/"
        return f"#"
    else:
        # fallback for other namespaces
        return f"#"

def format_image_path(item_id):
    name = item_id.split(":")[-1]
    return f"items/{name}.png"

def process_file(path):
    with open(path) as f:
        data = json.load(f)
    rtype = data.get("type", "")
    normalized_type = normalize_recipe_type(rtype)
    if not normalized_type:
        return None
    if normalized_type == "shaped":
        grid = parse_shaped(data)
    else:
        grid = parse_shapeless(data)
    result = parse_result(data)
    recipe_id = os.path.splitext(os.path.basename(path))[0]
    table = data.get("table")
    title = get_recipe_title(rtype, table, result["item"])
    recipe_data = {
        "title": title,
        "grid": grid,
        "output": result,
        "type": normalized_type
    }
    return recipe_id, recipe_data

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Merge and flatten tags
    all_tagsList = merge_tag_folders(TAG_FOLDERS)
    flat_tags = flatten_tags(all_tagsList)

    # Collect recipes
    recipes = {}
    with open(OUTPUT_TAGS_FILE, "w") as f:
        json.dump(flat_tags, f, indent=2)
 
    for folder in [LOTR_RECIPES, EXTENDED_RECIPES]:
        if not os.path.exists(folder):
            continue
        for file in os.listdir(folder):
            if not file.endswith(".json"):
                continue
            res = process_file(os.path.join(folder, file))
            if res:
                rid, data = res
                recipes[rid] = data

    # Collect all item IDs from recipes and tags
    all_items = set()
    for r in recipes.values():
        for row in r["grid"]:
            for ing in row:
                if ing and not ing.startswith("#"):
                    all_items.add(ing)
        out = r["output"]
        all_items.add(out["item"])

    existing_items = {}
    if os.path.exists(OUTPUT_ITEMS_FILE):
        try:
            with open(OUTPUT_ITEMS_FILE, "r") as f:
                existing_items = json.load(f)
        except Exception as e:
            log.warning(f"Failed to load existing items.json: {e}")
            
    items_data = existing_items.copy()
    for item in sorted(all_items):
        generated = {
            "name": format_item_name(item),
            "tooltip": format_item_name(item),
            "url": format_item_url(item),
            "image": format_image_path(item)
        }

        if item not in items_data:
            items_data[item] = generated
        else:
            # Fill only missing fields, keep manual edits
            for key, value in generated.items():
                if key not in items_data[item] or not items_data[item][key]:
                    items_data[item][key] = value

    # Validate recipes
    valid_recipes = {k: v for k, v in recipes.items() if validate_recipe(v, all_items, flat_tags, k)}

    # Filter unused tags recursively
    resolved_tags = filter_unused_tags(flat_tags, valid_recipes)

    # Sort items inside item data
    FIELD_ORDER = ["name", "tooltip", "image", "url"]
    reordered_items = {}
    
    for item_id, data in items_data.items():
        new_entry = {}
        # Add fields in desired order
        for field in FIELD_ORDER:
            if field in data:
                new_entry[field] = data[field]
        # Preserve any extra/custom fields (put them at the end)
        for field in data:
            if field not in FIELD_ORDER:
                new_entry[field] = data[field]
        reordered_items[item_id] = new_entry
    items_data = reordered_items

    # Sort recipes, tags, and items alphabetically by key
    sorted_recipes = dict(sorted(valid_recipes.items()))
    sorted_tags = dict(sorted(resolved_tags.items()))
    items_data = dict(sorted(items_data.items()))

    # Save output
    with open(OUTPUT_RECIPES_FILE, "w") as f:
        json.dump(sorted_recipes, f, indent=2)
    with open(OUTPUT_TAGS_FILE, "w") as f:
        json.dump(sorted_tags, f, indent=2)
    with open(OUTPUT_ITEMS_FILE, "w") as f:
        json.dump(items_data, f, indent=2)
    print(f"Generated {len(items_data)} items, {len(valid_recipes)} recipes, and {len(resolved_tags)} tags.")

if __name__ == "__main__":
    main()