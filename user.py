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
