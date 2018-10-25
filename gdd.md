#GDD

This GDD (Game Design Document) documents the thinking that is going into this
prototype.  The intention is to write down the design goals so that I can make
a better game.

##Overview

Allies_RL (name pending) is a a fantasy anime themed roguelike.  The core
mechanic is a focus on gathering allies.  Each ally will be a full character
with dialogue, individual traits, and gameplay progression.

###Allies

####Introductions:

1) Start with one (you get to choose 1 thing to bring with you, you can bring
   your imouto if you want)
2) Save one from a monster attack.  You encounter them fighting with a monster,
   defeat the monster and they'll fall in love.
3) Encounter them normally (maybe with an existing party) and use dialogue to
   convince them to join you.
4) Summon them using a summon scroll (only way to get demons or other isekaijin)
5) Encounter them as prisoners to a bad guy or in a jail cell.  Save them by
   defeating the bad guy or by unlocking the jail cell.

####Personality:

1) Himesama - Stuck-up princess from a faraway land
2) Tsundere - Seems like a jerk at first but is really just shy
3) Yandere - Psychotic overpossessive nympho
4) Genki - Always happy and optimistic
5) Kuudere - Isn't strongly driven by emotions at all
6) Deredere - Affectionate and lovey-dovey

####Class:

1) Mage
2) Healer
3) Warrior
4) Archer

####Race:

Unique races and monster girl types will be a key method of creating rare,
desireable ally types.  

####Progression:

Primary progression is based on levels.  Each class gets new abilities at each
level.  Levels go from 1 to 10, at level 10 they become a Legendary whatever.

While there is no limit on the number of allies you can have, a larger harem
will create more stress.  Stress must be managed or your harem will collapse.

Secondary progression is in romance.  Giving gifts that characters like will
improve the romance progression, up to and including marriage.  Romance will
provide very powerful benefits, notably increased exp gain, unique skills such
as "protect", and unlocking various actions that temporarily raise personal
stats.  However, romance and intimate actions will raise the stress of other
allies, quickly leading to harem collapse.

###Dungeon

Allies_RL is a dungeon crawler.  MVP:  start in a dungeon, make your way to the
bottom.  Later:  Maybe have multiple dungeons to journey about, world map,
shops, etc.  Allies will follow basic orders which can be managed manually but
otherwise be controlled by AI.

The dungeon will contain randomly generated structure, allies, monsters, loot,
traps, among other things

####Structures

MVP: basic rooms.
Later:  something actually interesting

####Allies

(see above)

####Monsters

Monsters will be based on JRPG conventions rather than D&D conventions.  Slimes
for example will be weak tutorial monsters rather than snot blobs like in D&D.
Boss monsters will exist, as will dire/great/unique monsters.  

####Loot

Items of the following types:
  -Weapons.  Swords, Staffs, Wands, Bows.  Keep it simple.  Can have
    enchantments and quality levels.
  -Armor.  No separate gloves, socks, hats, whatever.  All just "armor".
  -Random monster-dropped crap.  Can be given as gifts to allies, sold to shop
    keepers, etc.
  -Gems.  Gems are consumables, basically potions and scrolls rolled into one.
    Their effects are known from the start.

####Traps

Traps will exist, probably.

####Other things

Not sure?  Maybe like hot springs or something

###UX/UI

Use 8-dir movement.  0-9 for skills (including spells, bow shots, etc.).
Self button/menu, Allies button/menu.

####Main interface:

|----------|------|
|          |status|
|   game   |      |
|          |      |
|----------|------|
| messages |  ?   |
|----------|------|

####Game

ASCII graphics, @ for player, & for ally (colored via hair color?)
Map is some cool ascii map or something?  Maybe get animation framework for
multi-tile animations.  Text box system for dialogue?

####Status

Shows status for you and allies.  Status overview is identical for everybody.
Probably health, mana, last action, conditions?

####Messages

Color-coded for sure.  Limit usage.  Make it so I can easily replace messages
with something on the screen?
