# Pip Imports
from copy import deepcopy
from itertools import combinations
from math import comb

# Script Imports
from methods import canCarry, canCraft, gatherNRecipes, gatherMaterials

# Asset Imports
from recipes import RECIPES

# Number of Items to Craft
TO_CRAFT = [0, 3, 8, 14, 24, 34, 45, 55, 70, 90, 110]
while True:
    TASK_TIER = int(input("What tier of the task are you on (1-10):\n"))
    if(TASK_TIER not in [1,2,3,4,5,6,7,8,9,10]):
        print("Please enter a valid tier")
    else:
        break

# Gather Carry Capacities
INVENTORY = { "weapon": 1, "armor": 1, "tool": 1, "bag": 1 }
while True:
    try:
        caps = input("Capacities (Slots, Materials, Mining, Fishing, Foods, Chopping, Bugs:\n")
        INVENTORY["slots"], INVENTORY["material"], INVENTORY["mining"], INVENTORY["fish"], INVENTORY["food"], INVENTORY["choppin"], INVENTORY["bug"] = [int(i) for i in caps.split(" ")]
        break
    except:
        print("Please enter a valid capacity input")
# Loop Through Combinations
FOUND = False
CRAFTABLE = [k for k, v in RECIPES.items() if v[1]]
TESTED = 0
POSSIBLE = comb(len(CRAFTABLE), TO_CRAFT[TASK_TIER])
for combo in combinations(iterable=CRAFTABLE, r=TO_CRAFT[TASK_TIER]):
    if(TESTED % 1000 == 0):
        print(f"Tested: { TESTED } / { POSSIBLE }", end="\r")
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
            # Print Recipes to Craft
            nl = "\n"
            pToCraft = {}
            for r in allRecipes:
                try:
                    pToCraft[r] += 1
                except KeyError:
                    pToCraft[r] = 1
            max_width = len(str(max(pToCraft.values())))
            printRecipes = [f"{v:{max_width}} {m}" for m, v in pToCraft.items()]
            print(f"\nRecipes:\n  { f'{nl}  '.join(printRecipes) }")
            # Print Materials Needed
            max_val = max(materialsCopy.values(),key=lambda x: x["quantity"])
            max_width = len(str(max_val["quantity"]))
            pMaterials = [f"{v['quantity']:{max_width}} {m}" for m, v in materialsCopy.items()]
            print(f"\nMaterials:\n  { f'{nl}  '.join(pMaterials) }")
            print(f"Can carry: { carry }")
            print(f"Can Craft: { craft }")
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
