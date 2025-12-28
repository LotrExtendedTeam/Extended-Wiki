---
show:
  - toc
---

# **Entity Settings**

Entity settings provide a JSON-driven way to modify the behavior and properties of entities, including **vanilla entities** and entities added by **other mods**, without directly modifying their source definitions.

Currently it allows for:  
- Assign factions to entities
- Applying bonus alignment rewards on kill
- Attaching speechbanks to entities for dialogue and interaction

Entity Settings are defined and configured using JSON files located within a data pack under:  
- `data/<namespace>/npcs/entity_settings/<entity>.json`  
- Where the `namespace` and `entity` fields are the entity's in-game `namespace:path` id.

## Entity Settings JSON format

Each entity type may define a single settings file describing that entities's settings.

<div class="display-tree">
  <ul>
    <li>
      The root object
      <ul>
        <li><strong>faction</strong>: <code>namespace:faction</code> (required)
          <ul>
            <li>The faction this entity belongs to.</li>
            <li>Used for alignment gain/loss and interaction logic.</li>
          </ul>
        </li>
        <li><strong>kill_bonus</strong>: <code>int</code> (default: <code>0</code>)
          <ul>
            <li>Alignment awarded when this entity is killed.</li>
            <li>Only written if greater than <code>0</code>.</li>
          </ul>
        </li>
        <li><strong>speechbank</strong>: <code>namespace:path</code> (default: <code>null</code>)
          <ul>
            <li>Speechbank used for dialogue, requires a full resource location path.</li>
            <li>If omitted, the entity will not have a speechbank set.</li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>

## Example entity settings

The following example assigns faction alignment, bonus alignment on kill, and a speech bank to an entity:

```json title="data/lotr/npcs/entity_settings/bree_brewer.json"
{
  "faction": "lotr:bree",
  "kill_bonus": 2,
  "speechbank": "lotrextended:bree/man"
}
```