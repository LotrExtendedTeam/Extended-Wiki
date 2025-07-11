---
show:
  - toc
---

# **Template pool**

A template pool is a structured collection of structure pieces used by Minecraft’s jigsaw structure system to procedurally generate complex structures in the world, such as villages, bastions, and custom modded structures.

Each structure piece within a template pool represents a structure template, which is a predefined NBT structure file containing blocks and entities to place.

During world generation, the jigsaw system randomly selects structure pieces from the pool, using weighted probabilities defined within the pool’s JSON configuration. This allows for variability and replayability, ensuring structures feel organic and diverse each time they generate.

Template pools are defined and configured using JSON files located within a data pack under:  
- `data/<namespace>/worldgen/template_pool`

Extended adds it's own jigsaw piece type in addition to Minecraft's [Jigsaw Pieces](https://minecraft.wiki/w/Template_pool#Pool_elements). This page documents the format of Extended's `lotrextended:extended_single_pool_element` type and how it integrates and differs from vanilla's `minecraft:single_pool_element`.

Pool JSON format
---

> The root tag
>
> > **fallback**: (required)
> >
> > - A fallback template pool `<namespace>/worldgen/template_pool/<path>`
> > - Used in the case structures in this pool can't generate.
> >
> > **elements**: A list of elements to randomly select from.
> > > An element.
> > > > **weight**: `int` (required)
> > > >
> > > > - How likely this element is to be chosen when using this pool. Value between 1 and 150 (inclusive).
> > > >
> > > > **element_type**: `namespace:type`(required)
> > > >
> > > > - The type of the pool element. See below.
> > > >
> > > > **projection**: `rigid` or `terrain_matching` (required)
> > > >
> > > > - Defines the terrain projection type. Can be `rigid` to place a fixed structure (like a house), or `terrain_matching` to match the terrain height (like a village road).
> > > > Additional fields are available depending on the spicific **element_type** defined.


Element JSON formats
---

**Vanilla Single Element**  
A pool element represents a single piece of a jigsaw structure.
> The element
>
> > **element_type**: `"minecraft:single_pool_element"` (required)
> >
> > - Identifies this as an extended single pool element.
> >
> > **projection**: See above (required)
> >
> > **location**: `example:flower_forest/village_house` (required)
> >
> > - The location of the structure file for this entry. Located in `data/<namespace>/structure/<path>`
> >
> > **processors**: `namespace:path_to_a_processor_list` (required)
> >
> > - The processor list applied before placement. See [Processor List](https://minecraft.wiki/w/Processor_list).
> > - Can be left as `"minecraft:empty"`

**Extended Single Pool Element**  
A pool element represents a single piece of a jigsaw structure but with additional fields to facilitate the needs of extended's structures.
> The element
>
> > **element_type**: `"lotrextended:extended_single_pool_element"` (required)
> >
> > - Identifies this as an extended single pool element.
> >
> > **projection**: See above (required)
> >
> > **location**: `example:flower_forest/village_house` (required)
> >
> > - The location of the structure file for this entry. Located in `data/<namespace>/structure/<path>` 
> >
> > **processors**: `namespace:path_to_a_processor_list` (required)
> >
> > - The processor list applied before placement. See [Processor List](https://minecraft.wiki/w/Processor_list).
> > - Can be left as `"minecraft:empty"`
> >
> > **max_place_distance**: `80` (default)
> >
> > - Maximum distance the structure can attempt to place blocks from its origin.
> > - **Only handled on the root structure piece**
> >
> > **max_depth**: `7` (default)
> >
> > - The maximum recursive generation depth when structures call children.
> > - **Only handled on the root structure piece**
> >
> > **shift_structure_up_by**: `0` (default)
> >
> > - The vertical offset (in blocks) to shift the structure upward during placement. A value of <code>0</code> will not apply any vertical offset.
> > - Additionaly a negative offset will shift the structure downwards during placement.
> > - This is used in the case that a structure should float off the ground, or the bottom the the structure is not at ground level part of the structure.
> > - **Only handled on the root structure piece**
> >
> > **chunk_corner_offset**: `7` (default)
> >
> > - The offset applied to chunk corner coordinates for centering structures on generation. (value between `0` and `15`).
> > - **Only handled on the root structure piece**
> >
> > **ignore_bb_checks**: `false` (default)
> >
> > - If `true`, bypasses bounding box intersection checks, allowing overlapping structures. When enabled, generates a minimal bounding box at the point of connection (used for things such as lampposts).
> > - **Disables having children**
> >
> > **apply_waterlogging**: `true` (default)
> >
> > - If `true`, liquids in the structure piece propergate through waterloggable blocks. If `false`, liquids are not allowed to spread.
> >
> > **blacklist_name**: `"NOTSET"` (default)
> >
> > - A custom identifier used for some pieces skip using the certian piece if another piece with the same blacklistable name was already spawned (used to have only one smithy in a village for example).
> >
> > **snap_to_water_height**: `false` (default)
> >
> > - If `true`, will attempt to align the structure piece's Y position to the water surface height (y=62) when generating.
> > 
> > **foundation_block**
> >
> > - Define a blockstate that is used as a foundation for a single piece structure (hopefully).
> >
> > > **Name**: `"minecraft:air"` (default)
> > >
> > > - Changing the field to anything but `minecraft:air` will effectively enable foundation placement.
> > >
> > > **Properties**: `Todo properly define` (default unset)
> > >
> > > - Holds a key-value pair repersentation of a non-default blockstate present in **Name**