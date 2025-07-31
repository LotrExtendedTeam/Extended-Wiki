import logging
import re
import markdown
from mkdocs.structure.pages import Page
log = logging.getLogger("mkdocs.plugins")

def on_pre_build(config):
    log.info(">>> Infobox Porcessor: Present")

def on_page_markdown(markdown_content, page: Page, config, files):

    INFOBOX_RE = re.compile(r'::infobox\n(.*?)\n::end-infobox', re.DOTALL)

    def markdown_to_html(text):
        """Convert markdown text to HTML, handling inline markdown elements."""
        if not text:
            return text
        # Create a markdown instance with common extensions
        md = markdown.Markdown(extensions=['extra', 'codehilite'])
        # Convert markdown to HTML and strip the wrapping <p> tags for inline content
        html = md.convert(text).strip()
        if html.startswith('<p>') and html.endswith('</p>') and html.count('<p>') == 1:
            html = html[3:-4]  # Remove wrapping <p></p> tags
        return html

    def render_infobox(match):
        block = match.group(1).strip()
        lines = block.splitlines()
        entries = {}
        for line in lines:
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                entries[key.lower()] = value

        title = entries.pop('title', 'Info')
        box_type = entries.pop('type', 'default')
        if(box_type=='default'):
            html = ['<div class="infobox">']
            html.append(f'<div class="infobox-header">Invalid Infobox</div>')
            html.append('</div>')
            return '\n'.join(html)
    
        image = entries.pop('image', None)
        image_alt = entries.pop('image_alt', title+' Image')
        footer = entries.pop('footer', '')
        footer_data = entries.pop('footer_data', '')

        html = ['<div class="infobox">']
        html.append(f'<div class="infobox-header">{title}</div>')

        if image:
            html.append('<div class="infobox-image">')
            html.append(f'<a href="/Extended-Wiki/wiki/img/{image}"><img src="/Extended-Wiki/wiki/img/{image}" alt="{image_alt}"></a>')
            html.append('</div>')

        if(box_type=='custom'):
            html.append('<div class="infobox-grid">')
            for key, value in entries.items():
                html.append('<div class="infobox-row">')
                html.append(f'<div class="label">{key.title()}</div>')
                html.append(f'<div class="value">{markdown_to_html(value)}</div>')
                html.append('</div>')
            html.append('</div>')
        else:
            if(box_type=='version'):
                if "changeloglink" in entries:
                    html.append('<div class="infobox-version-wrapper">')
                    #html.append(f'<div><strong>v{entries.get("name", "Unknown")}</strong></div>')
                    html.append(f'<div><a href="{entries["changeloglink"]}"><strong>v{entries.get("name", "Unknown")}</strong></a></div>')
                else:
                    html.append('<div class="infobox-version-wrapper">')
                    html.append(f'<div><strong>v{entries.get("name", "Unknown")}</strong></div>')
                if "date" in entries:
                    html.append(f'<div><em>Published {entries["date"]}</em></div>')
                    html.append('<div class="version-spacer"></div>')
                if "curseforgelink" in entries:
                    html.append(f'<div><a href="{entries["curseforgelink"]}">Curseforge</a></div>')
                if "modrinthlink" in entries:
                    html.append(f'<div><a href="{entries["modrinthlink"]}">Modrinth</a></div>')
                if "changeloglink" in entries:
                    html.append('<div class="version-spacer"></div>')
                    html.append(f'<div><a href="{entries["changeloglink"]}">Changelog</a></div>')
                html.append('</div>')
            else:
                grid_fields = {}
                if(box_type=='block'):
                    grid_fields = {
                        'rarity': 'Rarity tier',
                        'tool': 'Tool',
                        'physics': 'Physics Type',
                        'renewable': 'Renewable',
                        'stack': 'Stackability',
                        'hardness': 'Hardness',
                        'resistance': 'Blast Resistance',
                        'luminous': 'Luminous',
                        'transparency': 'Transparent',
                        'flammable': 'Flammable',
                    }
                elif(box_type=='item'):
                    grid_fields = {
                        'rarity': 'Rarity tier',
                        'tab': 'Tab',
                        'renewable': 'Renewable',
                        'stack': 'Stackability',
                    }
                elif(box_type=='armor'):
                    grid_fields = {
                        'rarity': 'Rarity tier',
                        'armor': 'Armor Points',
                        'toughness': 'Toughness',
                        'renewable': 'Renewable',
                        'stack': 'Stackability',
                    }
                elif(box_type=='entity'):
                    grid_fields = {
                        'armor': 'Armor Points',
                        'hitpoints': 'Hit Points',
                        'faction': 'Faction',
                    }
                elif(box_type=='tool'):
                    grid_fields = {
                        'rarity': 'Rarity tier',
                        'tab': 'Tab',
                        'damage': 'Damage',
                        'speed': 'Speed',
                        'reach': 'Reach',
                        'knockback': 'Knockback Bonus',
                        'durability': 'Durability',
                        'renewable': 'Renewable',
                        'stack': 'Stackability',
                    }
                elif(box_type=='food'):
                    grid_fields = {
                        'rarity': 'Rarity tier',
                        'saturation': 'Saturation',
                        'hunger': 'Restores',
                        'renewable': 'Renewable',
                        'stack': 'Stackability',
                    }
                html.append('<div class="infobox-grid">')
                for key, label in grid_fields.items():
                    if key in entries:
                        value = entries[key]
                        html.append('<div class="infobox-row">')
                        html.append(f'    <div class="label">{label}</div>')
                        html.append(f'    <div class="value">{markdown_to_html(value)}</div>')
                        html.append('</div>')
                html.append('</div>')
        if footer:
            html.append(f'<div class="infobox-footer">{footer}</div>')
        if footer_data:
            html.append(f'<div class="infobox-footer-data">{footer_data}</div>')
        html.append('</div>')
        return '\n'.join(html)

    new_markdown = INFOBOX_RE.sub(render_infobox, markdown_content)
    return new_markdown