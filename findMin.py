# Pip Imports
from copy import deepcopy
from itertools import combinations, combinations_with_replacement
from json import dump
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
CAP_TYPES = ["material", "mining", "fish", "food", "choppin", "bug"]
MULTIPLIERS = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
SLEEP_TIME = 0.01
SLOTS = range(16,65)
TIERS = [0, 3, 8, 14, 24, 34, 45, 55, 70, 90, 110]

# Pull, Score, Sort Recipes
CRAFTABLE = [k for k, v in RECIPES.items() if v[1]]
SCORED_RECIPES = scoreRecipes(toCraft=CRAFTABLE)

RECOMMENDATIONS = []
for ti, t in enumerate(TIERS):
    if(ti == 0):
        RECOMMENDATIONS.append(None)
        continue
    print(f"Processing Tier {ti}: {t} Items\n")
    # Pull recipes and materials
    tierRecipes = sortRecipes(toCraft=SCORED_RECIPES[:t], n=t, recipes=RECIPES)
    materials = gatherMaterials(toCraft=tierRecipes, recipes=RECIPES)
    # Process caps needed
    capsNeeded = {
        "material": False, "mining": False, "fish": False,
        "food": False, "choppin": False, "bug": False
    }
    for m, info in materials.items():
        mType = info["type"]
        if(mType in CAP_TYPES):
            capsNeeded[mType] = True
    nCaps = len([1 for _,v in capsNeeded.items() if v])
    # Setup Inventory and Mintventory
    inventory = { 
        "slots": 16, "material": 10, "mining": 10, "fish": 10,
        "food": 10, "choppin": 10, "bug": 10,
        "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000
    }
    minventory = { 
        "slots": 100000, "material": 100000, "mining": 100000, "fish": 100000,
        "food": 100000, "choppin": 100000, "bug": 100000,
        "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000
    }
    # Loop through various slots
    found = []
    for s in SLOTS:
        # Set number of slots
        inventory["slots"] = s
        # Check P2W Multipliers ( last )
        for m in MULTIPLIERS:
            # Check cap permutations
            for p in combinations_with_replacement(BASE_CAPS, nCaps):
                # Update Inventory
                pi = 0
                for cap in ("material", "mining", "fish", "food", "choppin", "bug"):
                    if(capsNeeded[cap]):
                        inventory[cap] = floor(p[pi] * m)
                        pi += 1
                # Status Message
                message = f"{ m }x  "
                message += f"Slots: { inventory['slots'] }  "
                message += f"Mat: { inventory['material'] }  "
                message += f"Min: { inventory['mining'] }  "
                message += f"Fsh: { inventory['fish'] }  "
                message += f"Fds: { inventory['food'] }  "
                message += f"Chp: { inventory['choppin'] }  "
                message += f"Bug: { inventory['bug'] }"
                print(message, end="\r")
                # Check if we can carry + craft
                if(canCarry(materials=deepcopy(materials), inventory=inventory)):
                    if(canCraft(toCraft=tierRecipes, materials=deepcopy(materials), recipes=RECIPES, inv=inventory)):
                        temp = (inventory["slots"], inventory["material"], inventory["mining"],
                                inventory["fish"], inventory["food"], inventory["choppin"],
                                inventory["bug"])
                        if(all([inventory[k] <= minventory[k] for k in inventory if k != "slots"])):
                            minventory = deepcopy(inventory)
        found.append(minventory)
    # Parse recipes
    compressed = []
    curRec, curCnt = None, 0
    for r in tierRecipes:
        # Update current recipe/counts
        if(curRec is None):
            curRec = r
            curCnt += 1
        elif(curRec == r):
            curCnt += 1
        else:
            compressed.append(f"{curCnt} {curRec}")
            curRec, curCnt = r, 1
    compressed.append(f"{curCnt} {curRec}")
    # Update Recommendations
    recommend = {
        "tier": ti, "items": t, "recipes": compressed,
        "materials": [f"{info['quantity']} {m}" for m, info in materials.items()], "caps": []
    }
    # Check if inventory should be added
    current = { 
        "slots": 16, "material": 10000, "mining": 10000, "fish": 10000,
        "food": 10000, "choppin": 10000, "bug": 10000,
        "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000
    }
    for i in found:
        if(i["slots"] == 100000):
            continue
        compare = [current[k] == i[k] for k in i if k != "slots"]
        if(not all(compare)):
            recommend["caps"].append({
                "slots": i["slots"], "material": i["material"],
                "mining": i["mining"], "fish": i["fish"],
                "food": i["food"], "choppin": i["choppin"],
                "bug": i["bug"]
            })
            current = deepcopy(i)
    RECOMMENDATIONS.append(recommend)

# Write to flatfile
with open("recommended.json", "w") as f:
    dump(RECOMMENDATIONS, f, indent=2)