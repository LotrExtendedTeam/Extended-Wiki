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
<div class="display-tree">
  <ul>
    <li>
      The root tag
      <ul>
        <li><strong>fallback</strong>: (required)
          <ul>
            <li>A fallback template pool <code>&lt;namespace&gt;/worldgen/template_pool/&lt;path&gt;</code></li>
            <li>Used in the case structures in this pool can't generate.</li>
            <li>Can be left as <code>minecraft:empty</code></li>
          </ul>
        </li>
        <li><strong>elements</strong>: A list of elements to randomly select from.
          <ul>
            <li>An element
              <ul>
                <li><strong>weight</strong>: <code>int</code> (required)
                  <ul>
                    <li>How likely this element is to be chosen when using this pool. Value between <code>1</code> and <code>150</code> (inclusive).</li>
                  </ul>
                </li>
                <li><strong>element_type</strong>: <code>namespace:type</code> (required)
                  <ul>
                    <li>The type of the pool element. See below.</li>
                  </ul>
                </li>
                <li><strong>projection</strong>: <code>rigid</code> or <code>terrain_matching</code> (required)
                  <ul>
                    <li>Defines the terrain projection type. Can be <code>rigid</code> to place a fixed structure (like a house), or <code>terrain_matching</code> to match the terrain height (like a village road).</li>
                    <li>Additional fields are available depending on the specific <strong>element_type</strong> defined.</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>

Element JSON formats
---

**Vanilla Single Element**  
A pool element represents a single piece of a jigsaw structure.
<div class="display-tree">
  <ul>
    <li>
      The element
      <ul>
        <li><strong>element_type</strong>: <code>minecraft:single_pool_element</code> (required)</li>
        <li><strong>projection</strong>: See above (required)</li>
        <li>
          <strong>location</strong>: <code>example:flower_forest/village_house</code> (required)
          <ul>
            <li>The location of the structure file for this entry. Located in <code>data/&lt;namespace&gt;/structure/&lt;path&gt;</code></li>
          </ul>
        </li>
        <li>
          <strong>processors</strong>: <code>namespace:path_to_a_processor_list</code> (required)
          <ul>
            <li>The processor list applied before placement. See <a href="https://minecraft.wiki/w/Processor_list">Processor List</a>.</li>
            <li> Can be left as <code>minecraft:empty</code></li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>


**Extended Single Pool Element**  
A pool element represents a single piece of a jigsaw structure but with additional fields to facilitate the needs of extended's structures.
<div class="display-tree">
  <ul>
    <li>
      The element
      <ul>
        <li><strong>element_type</strong>: <code>lotrextended:extended_single_pool_element</code> (required)
          <ul>
            <li>Identifies this as an extended single pool element.</li>
          </ul>
        </li>
        <li><strong>projection</strong>: See above (required)</li>
        <li><strong>location</strong>: <code>example:flower_forest/village_house</code> (required)
          <ul>
            <li>The location of the structure file for this entry. Located in <code>data/&lt;namespace&gt;/structure/&lt;path&gt;</code></li>
          </ul>
        </li>
        <li><strong>processors</strong>: <code>namespace:path_to_a_processor_list</code> (required)
          <ul>
            <li>The processor list applied before placement. See <a href="https://minecraft.wiki/w/Processor_list">Processor List</a>.</li>
            <li>Can be left as <code>minecraft:empty</code></li>
          </ul>
        </li>
        <li><strong>max_place_distance</strong>: <code>80</code> (default)
          <ul>
            <li>Maximum distance the structure can attempt to place blocks from its origin.</li>
            <li><strong>Only handled on the root structure piece</strong></li>
          </ul>
        </li>
        <li><strong>max_depth</strong>: <code>-1</code> (default)
          <ul>
            <li>The maximum recursive generation depth when structures call children.</li>
            <li>The structure generator sets a default value of 7; giving the piece a value other than -1 will override the generator value.</li>
            <li><strong>Only handled on the root structure piece</strong></li>
          </ul>
        </li>
        <li><strong>chunk_corner_offset</strong>: <code>7</code> (default)
          <ul>
            <li>The offset applied to chunk corner coordinates for centering structures on generation. (value between 0 and 15).</li>
            <li><strong>Only handled on the root structure piece</strong></li>
          </ul>
        </li>
        <li><strong>ground_level_delta</strong>: <code>1</code> (default)
          <ul>
            <li>The vertical offset (in blocks) to shift the structure piece downwards during placement. A value of <code>1</code> will apply the regular vanilla offset.</li>
            <li>Additionally, a negative offset will shift the structure upwards during placement.</li>
            <li>This is used in the case that a structure should float off the ground, or the bottom of the structure is not at ground level.</li>
            <li>(This hooks into an unused method in vanilla that defaults to shifting a piece down by 1)</li>
          </ul>
        </li>
        <li><strong>ignore_bb_checks</strong>: <code>false</code> (default)
          <ul>
            <li>If true, bypasses bounding box intersection checks, allowing overlapping structures. When enabled, generates a minimal bounding box at the point of connection (used for things such as lampposts).</li>
            <li><strong>Disables having children</strong></li>
          </ul>
        </li>
        <li><strong>apply_waterlogging</strong>: <code>true</code> (default)
          <ul>
            <li>If true, liquids in the structure piece propagate through waterloggable blocks. If false, liquids are not allowed to spread.</li>
          </ul>
        </li>
        <li><strong>blacklist_name</strong>: <code>NOTSET</code> (default)
          <ul>
            <li>A custom identifier used for some pieces to skip using the certain piece if another piece with the same blacklistable name was already spawned. (Used to have only one smithy in a village, for example.)</li>
          </ul>
        </li>
        <li><strong>snap_to_water_height</strong>: <code>false</code> (default)
          <ul>
            <li>If true, will attempt to align the structure piece's Y position to the water surface height (y=62) when generating, if projecting to heightmap.</li>
          </ul>
        </li>
        <li><strong>should_protect_y_level</strong>: <code>true</code> (default)
          <ul>
            <li>If true, piece will not be used if it attempts to spawn below <code>protectable_y_level</code>.</li>
          </ul>
        </li>
        <li><strong>protectable_y_level</strong>: <code>12</code> (default)
          <ul>
            <li>The minimum height at which the piece can spawn. (Used to disable pieces from spawning too deep, and breaking bedrock.)</li>
          </ul>
        </li>
        <li><strong>reset_max_depth</strong>: <code>false</code> (default)
          <ul>
            <li>If true, the current depth stack (relative to max-depth) will be reset to zero.</li>
            <li><strong>Only applicable to non-root pieces</strong></li>
          </ul>
        </li>
        <li><strong>disable_spawn_above_ground</strong>: <code>false</code> (default)
          <ul>
            <li>If true, the piece will not spawn if the center of the placement is at or above ground level. (Used to stop mineshafts from spawning above ground.)</li>
            <li><strong>Only applicable to non-root pieces</strong></li>
          </ul>
        </li>
        <li><strong>foundation_block</strong>
          <ul>
            <li><strong>Name</strong>: <code>minecraft:air</code> (default)
              <ul>
                <li>Changing the field to anything but <code>minecraft:air</code> will effectively enable foundation placement.</li>
              </ul>
            </li>
            <li><strong>Properties</strong>: Todo properly define (default unset)
              <ul>
                <li>Holds a key-value pair representation of a non-default blockstate present in <strong>Name</strong></li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>