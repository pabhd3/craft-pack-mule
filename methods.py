# Pip Imports
from math import ceil


def gatherNRecipes(toCraft, recipes):
    """
        Recursively determine all recipes needed for starting list
        Input: toCraft=list(str), recipes=dict
        Returns: list(str)
    """
    allRecipes = [r for r in toCraft]
    nestedRecipes = []
    for recipe in toCraft:
        for rscName, rscCount, _, rscNested in recipes[recipe][2]:
            if(rscNested):
                nestedRecipes += gatherNRecipes(toCraft=[rscName]*rscCount, recipes=recipes)
    return nestedRecipes + allRecipes


def sortRecipes(toCraft, n, recipes):
    """
        Sort list of recipes based on quantity of resources needed to craft
        Inputs: toCraft=list(str), n=int, recipes=dict
        Returns: list(str)
    """
    # Setup list of main and nested recipes
    mainRec, nestRec = [], []
    for tc in toCraft:
        mainRec.append(tc)
        nested = set(gatherNRecipes(toCraft=[tc], recipes=recipes))
        # Check fi nested recipe was a "main" recipe
        for nr in nested:
            if(nr != tc):
                if(nr in mainRec):
                    # Add and remove main nested recipe
                    mainRec.remove(nr)
                    nestRec.append(nr)
        if((len(mainRec) +len(nestRec)) >= n):
            break
    counted = []
    for tc in mainRec:
        # Determine nested recipes + resources to craft them
        nested = gatherNRecipes(toCraft=[tc], recipes=recipes)
        needed = sum([sum([rsc[1] for rsc in recipes[nr][2]]) for nr in nested])
        counted.append((nested, needed))
    # Sort recipes by resources needed
    sortedRecipes = []
    for r in sorted(counted, key=lambda x: x[1], reverse=True):
        sortedRecipes += r[0]
    return sortedRecipes


def gatherMaterials(toCraft, recipes):
    """
        Determine list of materials/quantities to craft 1 of each recipe
        Input: recipes=list(str)
        Returns: dict
    """
    # Check for materials
    materials = {}
    for recipe in toCraft:
        rType, rCraftable, rResources, _ = recipes[recipe]
        for rscName, rscQuantity, rscType, RscRecipe in rResources:
            # Add material quantity
            if(not RscRecipe):
                try:
                    materials[rscName]["quantity"] += rscQuantity
                except KeyError:
                    materials[rscName] = { "type": rscType, "quantity": rscQuantity }
    return materials


def canCarry(materials, inventory):
    """
        Determine if a list of materials can be carried in inventory
        Input: materials=dict
        Returns: bool
    """
    slotsUsed = 0
    for material, info in materials.items():
        slots = ceil(info["quantity"] / inventory[info["type"]])
        slotsUsed += slots
    return slotsUsed <= inventory["slots"] - 1


def canCraft(toCraft, materials, recipes, inv):
    """
        Determine if a list of recipes can be crafted
        Inputs: toCraft=list(str), materials=dict, recipes=dict, inv=dict
        Returns: bool
    """
    # Setup Inventory
    inventory = [ None ] * inv["slots"]
    for material, info in materials.items():
        while True:
            # Find first empty slot
            idx = inventory.index(None)
            matType = info["type"]
            matQuantity = info["quantity"]
            slot = {
                "material": material,
                "quantity": inv[matType] if matQuantity > inv[matType] else matQuantity
            }
            inventory[idx] = slot
            # Update material quantity remaining
            info["quantity"] -= slot["quantity"]
            if(info["quantity"] == 0):
                break
    try:
        for recipe in toCraft:
            # Add crafted item
            rIndex = inventory.index(None)
            inventory[rIndex] = { "material": recipe, "quantity": 1 }
            # Remove Resources
            for rscName, rscNeeded, _, _ in recipes[recipe][2]:
                rscRemoved = 0
                while rscRemoved < rscNeeded:
                    rscStillNeeded = rscNeeded - rscRemoved
                    # Find resource index
                    rscIndex = [None if i is None else i["material"]
                                for i in inventory].index(rscName)
                    if(inventory[rscIndex]["quantity"] > rscStillNeeded):
                        # Remove whats needed
                        rscRemoved += rscStillNeeded
                        inventory[rscIndex]["quantity"] -= rscStillNeeded
                    elif(rscStillNeeded >= inventory[rscIndex]["quantity"]):
                        # Remove all from inventory index
                        rscRemoved += inventory[rscIndex]["quantity"]
                        inventory[rscIndex] = None
            # Cleanup Inventory
            matList = [None if m is None else m["material"] for m in inventory]
            for material in set([m["material"] for m in inventory 
                                 if m is not None and m["material"] not in toCraft]):
                # Parse material type and inventory indexes
                matType = materials[material]["type"]
                matIdxs = [i for i, d in enumerate(matList) if d == material]
                # Check for 2+ slots used can be reduced
                if(len(matIdxs) > 1):
                    matQuantities = [inventory[i]["quantity"] for i in matIdxs]
                    if(ceil(sum(matQuantities)/inv[matType]) < len(matIdxs)):
                        # Set current slots to empty
                        for i in matIdxs:
                            inventory[i] = None
                        matToPlace = sum(matQuantities)
                        while True:
                            # Find an empty slot
                            idx = inventory.index(None)
                            slot = {
                                "material": material,
                                "quantity": inv[matType] if matToPlace > inv[matType] else matToPlace
                            }
                            inventory[idx] = slot
                            # Update materials quantity remaining
                            matToPlace -= slot["quantity"]
                            if(matToPlace == 0):
                                break
        return True
    except Exception as err:
        return False


def recipeMaterials(r, recipes):
    nested = gatherNRecipes(toCraft=r, recipes=recipes)
    materials = gatherMaterials(toCraft=nested, recipes=recipes)
    print(materials)