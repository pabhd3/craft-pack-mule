# Pip Imports
from copy import deepcopy
from itertools import combinations
from math import comb
from re import findall

# Script Imports
from methods import canCarry, canCraft, gatherMaterials, gatherNRecipes, sortRecipes
from scoreRecipes import scoreRecipes
import user

# Asset Imports
from recipes import RECIPES

def findCombo():
    # Number of Items to Craft
    TO_CRAFT = [0, 3, 8, 14, 24, 34, 45, 55, 70, 90, 110]
    TASK_TIER = user.getTaskTier()

    # Gather Carry Capacities
    INVENTORY = { "weapon": 1, "armor": 1, "tool": 1, "bag": 1, "inf": 100000 }
    user.getCaps(inventory=INVENTORY)

    # Loop Through Combinations
    FOUND = False
    CRAFTABLE = scoreRecipes(toCraft=[k for k, v in RECIPES.items() if v[1]])
    TESTED = 0
    POSSIBLE = comb(len(CRAFTABLE), TO_CRAFT[TASK_TIER])
    CONTINUING = False
    for combo in combinations(iterable=CRAFTABLE, r=TO_CRAFT[TASK_TIER]):
        if(TESTED % 1000 == 0):
            pPossible = POSSIBLE if CONTINUING else 10000
            print(f"Tested: { TESTED } / { pPossible }", end="\r")
        if(TESTED == 10000):
            user.printRecommended(tier=TASK_TIER)
            if(input("Would you like to keep searching for combos (y/n)?:\n") == "y"):
                CONTINUING = True
                pass
            else:
                break
        # Gather recipe list, material list, and simulate carrying
        allRecipes = sortRecipes(toCraft=combo, n=TO_CRAFT[TASK_TIER], recipes=RECIPES)
        materials = gatherMaterials(toCraft=allRecipes, recipes=RECIPES)
        carry = canCarry(materials=materials, inventory=INVENTORY)
        # Make copy of materials
        materialsCopy = deepcopy(materials)
        if(carry):
            # Simulate crafting
            craft = canCraft(toCraft=allRecipes, materials=materials, recipes=RECIPES, inv=INVENTORY)
            if(craft):
                FOUND = True
                user.printCombo(recipes=allRecipes, materials=materialsCopy)
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

# Reminder to look at README
print(f"A README is available in the 'code > README.md' section of this Repl\n")

# Loop through options
option2Prompt = f"\nEnter the recipe ( quantity optional ) as it appears "\
                f"in-game:\nEx. 'Sizable Choppin Pouch' or 'Icing Ironbite 25': "
while(True):
    print(f"\n\n1. Solve Pack Mule Crafter Task Tier")
    print(f"2. Find Materials for a Recipe")
    print(f"3. Exit")
    menuChoice = input(f"Welcome to the Legends of Idleon Pack Mule Crafter tool, choose an option:\n")
    if(menuChoice == "1"):
        findCombo()
    elif(menuChoice == "2"):
        # Get recipe to craft
        recipeCount = findall(r"(\D+) ?(\d*)", input(option2Prompt))
        uRcp, uCnt = "DoesNotExist", 1
        try:
            # Parse recipe and quantity to make
            uRcp = recipeCount[0][0].strip()
            uCnt = int(recipeCount[0][1])
            if(uCnt < 1):
                uCnt = 1
        except:
            uCnt = 1
        finally:
            print(f"Crafting: '{ uRcp }' x{ uCnt }")
        try:
            # Try accessing it
            RECIPES[uRcp]
            # Gather recipes, materials, and report
            nestedRecipes = gatherNRecipes(toCraft=[uRcp]*uCnt, recipes=RECIPES)
            nestedMaterials = gatherMaterials(toCraft=nestedRecipes, recipes=RECIPES)
            user.printCombo(recipes=nestedRecipes, materials=nestedMaterials)
        except KeyError:
            print(f"\nRecipe not found\nDid you mean any of these recipes?")
            s = uRcp[:3]
            suggest = [k for k in RECIPES.keys() if s.lower() in k.lower()]
            print("\n  ".join(suggest))
    elif(menuChoice == "3"):
        break
    else:
        print(f"Please enter a valid choice...")
