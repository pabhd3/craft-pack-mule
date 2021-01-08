# Pip Imports
from json import load

# Load Assets
with open("recommended.json", "r") as f:
    RECOMMENDED = load(f)


def getTaskTier():
    """
        Get task tier from user via input
        Returns: int
    """
    while True:
        TASK_TIER = int(input("What tier of the task are you on (1-10):\n"))
        # Validate input
        if(TASK_TIER not in [1,2,3,4,5,6,7,8,9,10]):
            print("Please enter a valid tier...")
        else:
            break
    return TASK_TIER


def getCaps(inventory):
    """
        Get slot and carry capacities from user via input
        Input: inventory=dict
    """
    while True:
        try:
            prompt = "Capacities (Slots, Materials, Mining, Fishing, Foods, Chopping, Bugs)\n"\
                     "Ex. 45 491 150 75 375 451 75:\n"
            caps = input(prompt)
            # Parse input
            (inventory["slots"], inventory["material"], inventory["mining"],
             inventory["fish"], inventory["food"], inventory["choppin"],
             inventory["bug"]) = [int(i) for i in caps.split(" ")]
            break
        except:
            print("Please enter a valid capacity input")


def compressRecipes(recipes):
    """
        Compress a list of recipes to print results
        Input: recipes=list(str)
        Returns: list(str)
    """
    # Setup list of recieps
    compressed = []
    curRec, curCnt = None, 0
    for r in recipes:
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
    return compressed


def printCombo(recipes, materials):
    """
        Print working recipe combo + materials
        Inputs: recipes=list(str), materials=dict
    """
    # Newline
    nl = "\n"
    compressed = compressRecipes(recipes=recipes)
    print(f"\nRecipes:\n  { f'{nl}  '.join(compressed) }")
    # Format Materials
    max_val = max(materials.values(),key=lambda x: x["quantity"])
    max_width = len(str(max_val["quantity"]))
    pMaterials = [f"{v['quantity']:{max_width}} {m}" for m, v in materials.items()]
    print(f"\nMaterials:\n  { f'{nl}  '.join(pMaterials) }")


def printRecommended(tier):
    """
    Print list of recommended recipes, materials, slots and caps for a
    given tier
    Input: tier=int
    """
    print(f"\n\nLooks like your carry capacity probably isn't enough for Tier { tier }.\n")
    print(f"Below is a list of recommended recipes, number of slots and cap limits:\n")
    # Pull recmmended info
    recommendedTier = RECOMMENDED[tier]
    compressed = compressRecipes(recipes=recommendedTier['recipes'])
    print(f"Recipes (Craft in Order)\n{ ', '.join(recommendedTier['recipes']) }\n")
    print(f"Materials\n{ ', '.join(recommendedTier['materials']) }\n")
    print(f"Inventory Setups:")
    if(recommendedTier["caps"]):
        for i in recommendedTier["caps"]:
            setup = f"* { i['slots'] } Slots, "\
                    f"{ i['material'] } Materials, "\
                    f"{ i['mining'] } Mining, "\
                    f"{ i['fish'] } Fish, "\
                    f"{ i['food'] } Food, "\
                    f"{ i['choppin'] } Chopping, "\
                    f"{ i['bug'] } Bug"
            print(setup)
    else:
        print("No current inventory setups exist for this list of recipes.")
    print("\nNote that these are recomendations that focus more on ease of "\
          "obtaining materials needed to craft them rather than the ease of "\
          "crafting them. These recommendations will be updated as more "\
          "recipes become available, and better methods to prioritize recipes "\
          "are found.\n")
