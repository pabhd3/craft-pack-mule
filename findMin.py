# Pip Imports
from copy import deepcopy
from itertools import combinations, combinations_with_replacement
from json import dump
from math import floor
from random import choice
from time import sleep

# Script Imports
from methods import canCarry, canCraft, gatherMaterials, sortRecipes
from scoreRecipes import scoreRecipes
from user import printCombo

# Asset Imports
from recipes import RECIPES

# Reference
ALL_ANVIL_TABS = [1, 2]
ALL_SLOTS = range(16,71)
ALL_TIERS = [0, 3, 8, 14, 24, 34, 45, 55, 70, 90, 110]

# Constants
ANVIL_TABS = [1, 2]
BASE_CAPS = [10, 50, 100, 250, 500]
CAP_TYPES = ["material", "mining", "fish", "food", "choppin", "bug"]
CONFIDENCE = 20
FLATFILE = "temp.json"
MAX_LOOPS = 100000
MAX_RECIPE_COMBOS = 10000
MULTIPLIERS = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
SLOTS = range(16,71)
STAMPS = set([round(s1*s2, 4) for s1, s2 in combinations([(1 + (x * 0.01)) for x in range(0, 51)], 2)])
TIERS = [0, 3, 8, 14, 24, 34, 45, 55, 70, 90, 110]

# Setup possible capacities
POSSIBLE_CAPS = set()
for base in BASE_CAPS:
    for multi in MULTIPLIERS:
        for stamp in STAMPS:
            pCap = floor(base * multi * stamp)
            POSSIBLE_CAPS.add(pCap)

def canCarryAndCraft(materials, recipes, inventory):
    """
    Determine if a list of recipes can be carried and crafted
    Inputs: materials=dict, recipes=list(str), inventory=dict
    Returns: bool
    """
    if(canCarry(materials=deepcopy(materials), inventory=inventory)):
        if(canCraft(toCraft=recipes, materials=deepcopy(materials),
                    recipes=RECIPES, inv=inventory)):
            return True
    return False

def findCraftable(n, scoredRecipes):
    """
    Determine if there are craftable combo of recipes
    Inputs: n=int, scoredRecipes=list(str)
    Returns: (bool, list(str), dict)
    """
    # Setup max inventory
    maxInventory = { 
        "slots": max(ALL_SLOTS), "material": max(POSSIBLE_CAPS),
        "mining": max(POSSIBLE_CAPS), "fish": max(POSSIBLE_CAPS),
        "food": max(POSSIBLE_CAPS), "choppin": max(POSSIBLE_CAPS),
        "bug": max(POSSIBLE_CAPS),
        "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000
    }
    # Setup trackers
    COMBOS_CHECKED = 0
    tierRecipes, materials = None, None
    for combo in combinations(iterable=scoredRecipes, r=t):
        # Generate recipes + materials
        tierRecipes = sortRecipes(toCraft=combo, n=t, recipes=RECIPES)
        materials = gatherMaterials(toCraft=tierRecipes, recipes=RECIPES)
        # Logging
        COMBOS_CHECKED += 1
        print(f"Checking Recipe Combos: {COMBOS_CHECKED}/{MAX_RECIPE_COMBOS}", end="\r")
        # Check if can be carried + crafted
        if(canCarryAndCraft(materials=materials, recipes=tierRecipes, inventory=maxInventory)):
            return (True, tierRecipes, materials)
        elif(COMBOS_CHECKED == MAX_RECIPE_COMBOS):
            return (False, None, None)

def updateCapRanges(capRanges, capNeeded):
    """
    Determine range of possible capacities to test in per carry type
    Inputs: capRanges=dict
    """
    for capType in capRanges:
        if(capType in capNeeded):
            # Determine Cap Percent
            CAP_PERCENT = round(1 - capRanges[capType]["recent"]/max(POSSIBLE_CAPS), 2)
            # Determine lower/upper, filter possible between and update
            lowerEnd, upperEnd = floor(CAP_PERCENT * capRanges[capType]["recent"]), capRanges[capType]["recent"]
            possible = [c for c in POSSIBLE_CAPS if (c >= lowerEnd and c <= upperEnd)]
            capRanges[capType]["possible"] = possible
            capRanges[capType]["lower"], capRanges[capType]["upper"] = min(possible), max(possible)
        else:
            capRanges[capType]["possible"] = [10]
            capRanges[capType]["lower"], capRanges[capType]["upper"] = 10, 10

RECOMMENDATIONS = {}
# Iterate Anvil Tabs + Task Tiers
for anvilTab in ANVIL_TABS:
    for ti, t in enumerate(TIERS):
        # Skip 0 items
        if(t == 0):
            continue
        print(f"\n\nProcessing Anvil Tab {anvilTab} Tier {ti}: {t} Items")
        # Set default recipes + materials
        CRAFTABLE = [k for k, v in RECIPES.items()
                     if v[1] and v[3] <= anvilTab]
        print(f"Available Recipes: {len(CRAFTABLE)}")
        tierRecipes, materials, found = [], [], []
        # Skip if not enough items or can't carry
        if(len(CRAFTABLE) >= t and t < max(ALL_SLOTS)):
            # Determine if there are craftable recipes
            SCORED_RECIPES = scoreRecipes(toCraft=CRAFTABLE)
            carryAndCraft, ccRecipes, ccMaterials = findCraftable(n=t, scoredRecipes=SCORED_RECIPES)
            if(carryAndCraft):
                # Update to carryable and craftable recipes/materials
                tierRecipes = deepcopy(ccRecipes)
                materials = deepcopy(ccMaterials)
                # Setup initial min inventory to max possible
                minventory = { 
                    "slots": max(ALL_SLOTS), "material": max(POSSIBLE_CAPS),
                    "mining": max(POSSIBLE_CAPS), "fish": max(POSSIBLE_CAPS),
                    "food": max(POSSIBLE_CAPS), "choppin": max(POSSIBLE_CAPS),
                    "bug": max(POSSIBLE_CAPS),
                    "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000
                }
                # Setup inventory
                inventory = { 
                    "slots": 16, "material": 10, "mining": 10, "fish": 10,
                    "food": 10, "choppin": 10, "bug": 10,
                    "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000
                }
                # Process caps needed
                capsNeeded = {
                    "material": False, "mining": False, "fish": False,
                    "food": False, "choppin": False, "bug": False
                }
                for m, info in materials.items():
                    mType = info["type"]
                    if(mType in CAP_TYPES):
                        capsNeeded[mType] = True
                capsNeededList = [k for k, v in capsNeeded.items() if v]
                print(f"Caps Needed: {capsNeededList}")
                # Loop through slots
                for slot in SLOTS:
                    # Check if carry/craftable at n slots
                    inventory["slots"] = slot
                    minventory["slots"] = slot
                    if(not canCarryAndCraft(materials=materials, recipes=tierRecipes, inventory=minventory)):
                        continue
                    # Update latest inventory
                    latest = (max(POSSIBLE_CAPS), max(POSSIBLE_CAPS), max(POSSIBLE_CAPS),
                              max(POSSIBLE_CAPS), max(POSSIBLE_CAPS), max(POSSIBLE_CAPS))
                    if(len(found) > 0):
                        latest = (found[-1]["material"], found[-1]["mining"], found[-1]["fish"],
                                  found[-1]["food"], found[-1]["choppin"], found[-1]["bug"])
                    # Move on if we can't do better
                    if(all([l == 10 for l in latest])):
                        continue
                    # Setup possible capacities per type
                    capTypeRanges = {
                        "material": { "lower": None, "upper": None, "recent": latest[0], "possible": [] },
                        "mining": { "lower": None, "upper": None, "recent": latest[1], "possible": [] },
                        "fish": { "lower": None, "upper": None, "recent": latest[2], "possible": [] },
                        "food": { "lower": None, "upper": None, "recent": latest[3], "possible": [] },
                        "choppin": { "lower": None, "upper": None, "recent": latest[4], "possible": [] },
                        "bug": { "lower": None, "upper": None, "recent": latest[5], "possible": [] }
                    }
                    updateCapRanges(capRanges=capTypeRanges, capNeeded=capsNeededList)
                    # Start searching
                    LOOPS, CHANGES, UPDATES = 0, 0, 0
                    while(LOOPS < MAX_LOOPS):
                        # Setup random inventory
                        for c in CAP_TYPES:
                            while(True):
                                temp = choice(capTypeRanges[c]["possible"])
                                if(temp <= capTypeRanges[c]["recent"]):
                                    inventory[c] = temp
                                    break
                        # Check if carry + craft
                        if(canCarryAndCraft(materials=materials, recipes=tierRecipes, inventory=inventory)):
                            # Check if improvement
                            if(all([inventory[k] <= minventory[k] for k in CAP_TYPES])):
                                # Update Minventory & latest
                                minventory = deepcopy(inventory)
                                latest = (inventory["material"], inventory["mining"], inventory["fish"],
                                        inventory["food"], inventory["choppin"], inventory["bug"])
                                # Update Possible Ranges
                                CHANGES += 1
                                # print(f"CHANGES: {CHANGES}")
                                for c in CAP_TYPES:
                                    capTypeRanges[c]["recent"] = inventory[c]
                                if(CHANGES == CONFIDENCE):
                                    CHANGES = 0
                                    if(any([capTypeRanges[c]["upper"] > capTypeRanges[c]["recent"] for c in CAP_TYPES])):
                                        updateCapRanges(capRanges=capTypeRanges, capNeeded=capsNeededList)
                                        UPDATES += 1
                        # Status message
                        if(LOOPS % 1000 == 0):
                            message = f"Slots: {slot} "\
                                    f" Mat: {capTypeRanges['material']['lower']}-{capTypeRanges['material']['upper']} "\
                                    f" Min: {capTypeRanges['mining']['lower']}-{capTypeRanges['mining']['upper']} "\
                                    f" Fsh: {capTypeRanges['fish']['lower']}-{capTypeRanges['fish']['upper']} "\
                                    f" Fod: {capTypeRanges['food']['lower']}-{capTypeRanges['food']['upper']} "\
                                    f" Chp: {capTypeRanges['choppin']['lower']}-{capTypeRanges['choppin']['upper']} "\
                                    f" Bug: {capTypeRanges['bug']['lower']}-{capTypeRanges['bug']['upper']} "\
                                    f"Loops: {LOOPS} Changes: {UPDATES}/{CHANGES}"
                            print(message, end="\r")
                        LOOPS += 1
                    print(minventory)
                    found.append(minventory)
        # Parse recipes
        compressed = []
        if(tierRecipes):
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
            "materials": [f"{info['quantity']} {m}"
                          for m, info in materials.items()]
                         if materials else [],
            "caps": []
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
        RECOMMENDATIONS[f"anvil{anvilTab}tier{ti}"] = recommend

# Write to flatfile
with open(FLATFILE, "w") as f:
    dump(RECOMMENDATIONS, f, indent=2)