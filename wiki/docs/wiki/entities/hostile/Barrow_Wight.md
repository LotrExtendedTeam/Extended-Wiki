---
tags:
  - Entities
show:
  - toc
alias:
  - barrow_wight
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

Barrow-wights are ancient, malevolent spirits that haunt the tombs and hills of the [[barrow_downs|Barrow Downs]]. Bound to cursed relics and burial mounds, they emerge to defend their domain from intruders.

## Spawning

Barrow-wights can appear in two primary ways: **natural spawning** and **stone chest spawning**.

### Natural Spawning
- Spawn naturally during **dusk and night**
- Only occurs in the [[barrow_downs|Barrow Downs]]

### Stone Chest Spawning

Barrow-wights may emerge when interacting with **stone chests**, depending on how the chest was created and the player’s status.

#### Player-Placed Chests
- Wights will **only** spawn if:
  - The chest is in the Barrow Downs  
  - The player is **cursed**

#### Naturally Generated Chests

Naturally generated chests follow special spawning rules:

- **Unopened Chests**
	- Have a **configurable chance** to spawn a Barrow-wight on first open  
	- Default chance: **50%**  
	- Config set behavior:
		- **0%** → Wights spawn *only* if the player is cursed  
		- **100%** → A Wight always spawns  
		- **1–99%** → Spawn chance is rolled when opened  
    - Additional rules:
        - If a Wight successfully spawns, the chest will never force another spawn  
        - If the spawn chance fails, the chest will retry the roll on the **next open**  
- **Previously Opened Chests**
	- If the chest already spawned a Wight via config chance:  
	- Future spawns require the player to be **cursed**  

## Behaviour

Barrow-wights are hostile to all creatures and will aggressively pursue targets within their detection radius. Once engaged, they will attempt to eliminate all nearby threats.

## Strategy

- Avoid opening stone chests while cursed
- Engage during daylight where possible to limit natural spawns
- Ranged combat is safer than melee encounters

## Lore

[Barrow-wights](https://tolkiengateway.net/wiki/Barrow-wights) are said to be spirits of ancient kings and warriors, corrupted and bound to their tombs by dark sorcery. They linger among the burial mounds, guarding cursed treasures and punishing those who disturb the dead.

## History

- 1.7.1: Fixed hitbox collision issues and revised chest spawning mechanics
- 1.7.0: Initial port

## Trivia

- Barrow-wights can be forced to spawn entirely through chest interaction
