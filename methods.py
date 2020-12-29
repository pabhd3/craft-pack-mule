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


def gatherMaterials(toCraft, recipes):
    """
        Determine list of materials/quantities to craft 1 of each recipe
        Input: recipes=list(str)
        Returns: dict
    """
    # Check for materials
    materials = {}
    for recipe in toCraft:
        rType, rCraftable, rResources = recipes[recipe]
        for rscName, rscQuantity, rscType, RscRecipe in rResources:
            # Add material quantity
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
        # Until material is empty
        while True:
            idx = inventory.index(None)
            matType = info["type"]
            matQuantity = info["quantity"]
            slot = {
                "material": material,
                "quantity": inv[matType] if matQuantity > inv[matType] else matQuantity
            }
            inventory[idx] = slot
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
                    rscIndex = [None if i is None else i["material"] for i in inventory].index(rscName)
                    if(inventory[rscIndex]["quantity"] > rscStillNeeded):
                        # Remove whats needed
                        rscRemoved += rscStillNeeded
                        inventory[rscIndex]["quantity"] -= rscStillNeeded
                    elif(rscStillNeeded >= inventory[rscIndex]["quantity"]):
                        # Remove all from inventory index
                        rscRemoved += inventory[rscIndex]["quantity"]
                        inventory[rscIndex] = None
        return True
    except Exception:
        return False
