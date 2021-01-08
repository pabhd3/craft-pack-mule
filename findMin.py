# Pip Imports
from copy import deepcopy
from itertools import combinations, combinations_with_replacement
from math import comb, floor
from time import sleep

# Script Imports
from methods import canCarry, canCraft, gatherMaterials, sortRecipes
from scoreRecipes import scoreRecipes
from user import printCombo

# Asset Imports
from recipes import RECIPES

# CONSTANTS
BASE_CAPS = [ 10, 50, 100, 250, 500, 1000 ]
CRAFTABLE = [k for k, v in RECIPES.items() if v[1]]
MULTIPLIERS = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
SLEEP_TIME = 0.01
SLOTS = range(16,65)
TO_CRAFT = 24


# Determine Caps Needed
CRAFTABLE = scoreRecipes(toCraft=CRAFTABLE)[:TO_CRAFT]
ALL_RECIPES = sortRecipes(toCraft=CRAFTABLE, recipes=RECIPES)
MATERIALS = gatherMaterials(toCraft=ALL_RECIPES, recipes=RECIPES)
CAPS_NEEDED = {
    "material": False, "mining": False, "fish": False,
    "food": False, "choppin": False, "bug": False
}
for m, info in MATERIALS.items():
    mType = info["type"]
    if(mType in ("material","mining","fish","food","choppin","bug")):
        CAPS_NEEDED[mType] = True
N_CAPS = len([1 for _,v in CAPS_NEEDED.items() if v])

# Setup Inventorys
INVENTORY = { 
    "slots": 16, "material": 10, "mining": 10, "fish": 10,
    "food": 10, "choppin": 10, "bug": 10,
    "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000
}
MINVENTORY = { 
    "slots": 100000, "material": 100000, "mining": 100000, "fish": 100000,
    "food": 100000, "choppin": 100000, "bug": 100000,
    "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000
}

# Print whatever
# print(f"Recipes\n{ ALL_RECIPES }\n")
# matList = []
# for m, info in MATERIALS.items():
#     matList.append(f"{ info['quantity'] } { m }")
# print(f"Materials\n{ matList }\n")
printCombo(recipes=ALL_RECIPES, materials=MATERIALS)
FOUND = []
for s in SLOTS:
    # Set number of slots
    INVENTORY["slots"] = s
    # Check P2W Multipliers ( last )
    for m in MULTIPLIERS:
        # Check cap permutations
        for p in combinations_with_replacement(BASE_CAPS, N_CAPS):
            # sleep(SLEEP_TIME)
            # Update Inventory
            pi = 0
            for cap in ("material", "mining", "fish", "food", "choppin", "bug"):
                if(CAPS_NEEDED[cap]):
                    INVENTORY[cap] = floor(p[pi] * m)
                    pi += 1
            # Status Message
            message = f"{ m }x  "
            message += f"Slots: { INVENTORY['slots'] }  "
            message += f"Mat: { INVENTORY['material'] }  "
            message += f"Min: { INVENTORY['mining'] }  "
            message += f"Fsh: { INVENTORY['fish'] }  "
            message += f"Fds: { INVENTORY['food'] }  "
            message += f"Chp: { INVENTORY['choppin'] }  "
            message += f"Bug: { INVENTORY['bug'] }"
            print(message, end="\r")
            # Check if we can carry + craft
            if(canCarry(materials=deepcopy(MATERIALS), inventory=INVENTORY)):
                if(canCraft(toCraft=ALL_RECIPES, materials=deepcopy(MATERIALS), recipes=RECIPES, inv=INVENTORY)):
                    temp = (INVENTORY["slots"], INVENTORY["material"], INVENTORY["mining"],
                            INVENTORY["fish"], INVENTORY["food"], INVENTORY["choppin"],
                            INVENTORY["bug"])
                    if(all([INVENTORY[k] <= MINVENTORY[k] for k in INVENTORY if k != "slots"])):
                        MINVENTORY = deepcopy(INVENTORY)
    FOUND.append(MINVENTORY)

# Print results
for p in FOUND:
    if(p["slots"] < 10000):
        print(p)



