# Pip Imports
from copy import deepcopy
from itertools import combinations
from math import comb

# Script Imports
from methods import canCarry, canCraft, gatherNRecipes, gatherMaterials
from user import getCaps, getTaskTier, printCombo

# Asset Imports
from recipes import RECIPES

# Number of Items to Craft
TO_CRAFT = [0, 3, 8, 14, 24, 34, 45, 55, 70, 90, 110]
TASK_TIER = getTaskTier()

# Gather Carry Capacities
INVENTORY = { "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000 }
getCaps(inventory=INVENTORY)

# Loop Through Combinations
FOUND = False
CRAFTABLE = [k for k, v in RECIPES.items() if v[1]]
TESTED = 0
POSSIBLE = comb(len(CRAFTABLE), TO_CRAFT[TASK_TIER])
for combo in combinations(iterable=CRAFTABLE, r=TO_CRAFT[TASK_TIER]):
    if(TESTED % 1000 == 0):
        print(f"Tested: { TESTED } / { POSSIBLE }", end="\r")
    if(TESTED == 10000):
        print(f"\n\nLooks like your carry capacity isn't enough for Tier { TASK_TIER }.")
        if(input("Would you like to keep searching for combos (y/n)?:\n") == "y"):
            pass
        else:
            break
    # Gather recipe list, material list, and simulate carrying
    allRecipes = gatherNRecipes(toCraft=combo, recipes=RECIPES)
    materials = gatherMaterials(toCraft=combo, recipes=RECIPES)
    carry = canCarry(materials=materials, inventory=INVENTORY)
    # Make copy of materials
    materialsCopy = deepcopy(materials)
    if(carry):
        # Simulate crafting
        craft = canCraft(toCraft=combo, materials=materials, recipes=RECIPES, inv=INVENTORY)
        if(craft):
            FOUND = True
            printCombo(recipes=allRecipes, materials=materialsCopy)
            if(FOUND):
                # Ask for another combo
                if(input(f"Find another recipe (y/n):\n") == "y"):
                    continue
                else:
                    break
            else:
              continue
    TESTED += 1
if(not FOUND):
    print(f"No recipe combinations found. Raise your carry capacity/slots and try again.")
