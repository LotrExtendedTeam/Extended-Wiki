---
tags:
  - Entities
show:
  - toc
---

####

::infobox
type: entity
title: Barrow Wight
image: entities/barrow_wight.png
armor: 6
hitpoints: 70
faction: Hostile
::end-infobox

# Barrow Wight

Barrow wights are evil spirits that reside in the barrow downs.

## Spawning

Barrow wights naturally spawn during dusk and night in the [Barrow Downs](/Extended-Wiki/wiki/Barrow_Downs/).

They also spawn via stone chests under certain conditions:

*  If a chest is placed by a player, Wights can only spawn from it if you are in the barrow downs, and cursed.
*  If a chest is naturally generated, there are two options:
  *  If the chest was never opened before, there is a server config-set chance to spawn. (Default value is a 50% chance)
     *  If config is 0, Wights only spawn when the player is cursed.
     *  If config is 100, a Wight will always spawn.
     *  Between these, wights will only spawn randomly, depending on the server config-set value.
     *  After initial spawn, the chest can't have anymore forced spawns (like legacy).
        * In addition, if the chest failed the random chance to force spawn, if will wait to spawn a Wight until the next open, at which point it will run the chance spawn check again. (So checking previously opened chests could spawn a Wight, depending on the server chance value not spawning one already)
  *  If the chest had previously been opened, and the the chest had successfully spawned a Wight by config set chance, then Wights will only spawn if the player is cursed.

## Behaviour

Barrow wights are hostile to all other creatures and will go out of their way to eliminate all in their radius.

## History

- 1.7.1: Fixed hitbox collisions issues and changed spawning mechanics from chests
- 1.7.0: Ported them

## Trivia

- IDk
