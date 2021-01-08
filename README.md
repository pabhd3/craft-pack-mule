# Legends of Idleon Blunderhills Pack Mule Crafter

This tool is used to determine various recipe combinations used to complete the Blunderhills Pack Mule Crafter task.

```
Up to date with Version 1.06
Task Tier Supported: 10
Recommendations Tier Supported: 6
Last Updated: Jan 07, 2020 18:10:00 CST
```

## Special Thanks

AlienC4#5271 ( Optimization )

Big Coight#4453, Deerjump#3003 ( Recipe data parsing)

## Default Locked Recipes

The following recipes are currently considered locked, either due to actually being uncraftable or my working on how to handle its recipe correctly.

```
Party Hat, Anvil Tab 2, Golden Peanut, Blunderhills NPC Completion Token, Blunder Skills Completion Token, Blunderhills Misc Completion Token, Easy Blunderhills NPC Token, Med Blunderhills NPC Token, Hard Blunderhills NPC Token, Anvil Tab 3, Empty Box
```

## How to use

Make sure to check the appropriate config files listed below, to make sure everything is set up correctly.

`Setting Task Tier`
After hitting run, you will be prompted to say which tier of the task you are currently on. See example below on how to input:

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

## Recommendations (Beta)

If after 10,000 combinations of recipes a working combo isn't found, you'll be provided with a list of recommendations to complete this current tier.

Please note that this feature is a *WORK IN PROGRESS*, and that it can be improved upon. Not every task tier is currently supported, but improvements are being made.

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