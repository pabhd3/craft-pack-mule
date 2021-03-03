# Legends of Idleon Blunderhills Pack Mule Crafter

This tool is used to determine various recipe combinations used to complete the Blunderhills Pack Mule Crafter task.

```
Up to date with Version 1.12
Task Tier Supported: 10
Recommendations Tier Supported: 6 ( 7 unverified )
Last Updated: Mar 3, 2020 09:09:00 CST

Contact Me: pabhd3#0802 ( Discord )
```

## Special Thanks

AlienC4#5271 ( Optimization )

Big Coight#4453, Deerjump#3003 ( Recipe data parsing )

Hellsent#3689 ( Testing )

LiuLangZhe#9086 ( Feature Suggestor )

## Default Locked Recipes

The following recipes are currently considered locked, either due to actually being uncraftable or my working on how to handle its recipe correctly.

```
Party Hat, Blunderhills NPC Completion Token, Blunder Skills Completion Token, Blunderhills Misc Completion Token, Easy Blunderhills NPC Token, Med Blunderhills NPC Token, Hard Blunderhills NPC Token, Anvil Tab 3
```

## How to use

Make sure to check the appropriate config files listed below, to make sure everything is set up correctly.

After hitting run, you will be prompted to choose an option listed below.

### Option 1 - Solve Pack Mule Crafter

`Setting Task Tier`
You will be prompted to say which tier of the task you are currently on. See example below on how to input:

```
What tier of the task are you on (1-10):
3
```

`Adding Capacities`

After hitting run, you will be prompted in the console to add in your inventory slots and carry capacities. See pictures ( s1.PNG and s2.PNG ) for values to use, and see example below on how to input capacities:

```
Capacities (Slots, Materials, Mining, Fishing, Foods, Chopping, Bugs)
Ex. 45 491 150 75 375 451 75:
39 491 150 75 375 431 75
```

### Option 2 - Craft a Recipe

You will be prompted to say and item, and an optional quanity to craft. See example below on how to input:

```
Sizable Choppin Pouch

Icing Ironbite 25

Buttered Toasted Butter

Studded Hide 2
```

Currently, number of inventory slots and carry capacities are not taken into account when calculating material costs.

## Recommendations (Beta)

If after 10,000 combinations of recipes a working combo isn't found, you'll be provided with a list of recommendations to complete this current tier.

Please note that this feature is a *WORK IN PROGRESS*, and that it can be improved upon. Not every task tier is currently supported, but improvements are being made.

### Calculations

The following are taken into account when calculating Recommendations (Beta):

* Inventory Slots: 16 - 68
* Inventory Bags: 10, 50, 100, 250, 500
* Inventory Multipliers: 1x - 3.5x
* Stamp Multipliers: 1x - 1.5x

## Unlocking Recipes

`File: recipes.py`

By default, the script will assume you can use all recipes. To set a recipe to be uncraftable, update the line to reflect the change with the following format:

_Recipe Unlocked Wooden Spear ( line 2 )_

```
"Wooden Spear": ("wpn",True,[("S...
```

_Recipe Locked Wooden Spear ( line 2 )_

```
"Wooden Spear": ("wpn",False,[("S...
```

Notice the _False_ included in the locked recipe. That is the only value you will change to make a recipe locked.