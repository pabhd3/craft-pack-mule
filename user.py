# Asset Imports
from recommended import RECOMMENDED


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
            caps = input("Capacities (Slots, Materials, Mining, Fishing, Foods, Chopping, Bugs:\n")
            # Parse input
            (inventory["slots"], inventory["material"], inventory["mining"],
             inventory["fish"], inventory["food"], inventory["choppin"],
             inventory["bug"]) = [int(i) for i in caps.split(" ")]
            break
        except:
            print("Please enter a valid capacity input")


def printCombo(recipes, materials):
    """
        Print working recipe combo + materials
        Inputs: recipes=list(str), materials=dict
    """
    # Newline
    nl = "\n"
    # Generate Recipe:Counts
    pToCraft = {}
    for r in recipes:
        try:
            pToCraft[r] += 1
        except KeyError:
            pToCraft[r] = 1
    # Format Recipes
    max_width = len(str(max(pToCraft.values())))
    printRecipes = [f"{v:{max_width}} {m}" for m, v in pToCraft.items()]
    print(f"\nRecipes:\n  { f'{nl}  '.join(printRecipes) }")
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
    print(f"Recipes\n{ ', '.join(recommendedTier['recipes']) }\n")
    print(f"Materials\n{ ', '.join(recommendedTier['materials']) }\n")
    print(f"Inventory Setups:")
    for i in recommendedTier["caps"]:
        setup = f"* { i['slots'] } Slots, "\
                f"{ i['material'] } Materials, "\
                f"{ i['mining'] } Mining, "\
                f"{ i['fish'] } Fish, "\
                f"{ i['food'] } Food, "\
                f"{ i['choppin'] } Chopping, "\
                f"{ i['bug'] } Bug"
        print(setup)
    print("\nNote that these are recomendations that focus more on ease of crafting "\
          "rather then ease of obtaining materials needed to craft them. These "\
          "recommendations will be updated as more recipes become available, and "\
          "better methods to prioritize recipes are found.\n")
