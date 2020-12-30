# Pip Imports
from math import ceil


def gather_n_recipes(to_craft, recipes):
    """
        Recursively determine all recipes needed for starting list
        Input: toCraft=list(str), recipes=dict
        Returns: list(str)
    """
    all_recipes = [r for r in to_craft]
    nested_recipes = []
    for recipe in to_craft:
        for rsc_name, rsc_count, _, rsc_nested in recipes[recipe][2]:
            if rsc_nested:
                nested_recipes += gather_n_recipes(to_craft=[rsc_name] * rsc_count, recipes=recipes)
    return nested_recipes + all_recipes


def gather_materials(to_craft, recipes):
    """
        Determine list of materials/quantities to craft 1 of each recipe
        Input: recipes=list(str)
        Returns: dict
    """
    # Check for materials
    materials = {}
    for recipe in to_craft:
        r_type, r_craftable, r_resources = recipes[recipe]
        for rsc_name, rsc_quantity, rsc_type, rec_recipe in r_resources:
            # Add material quantity
            try:
                materials[rsc_name]["quantity"] += rsc_quantity
            except KeyError:
                materials[rsc_name] = {"type": rsc_type, "quantity": rsc_quantity}
    return materials


def can_carry(materials, inventory):
    """
        Determine if a list of materials can be carried in inventory
        Input: materials=dict
        Returns: bool
    """
    slots_used = 0
    for material, info in materials.items():
        slots = ceil(info["quantity"] / inventory[info["type"]])
        slots_used += slots
        if slots_used >= inventory["slots"]:
            return False
    return slots_used < inventory["slots"]


def can_craft(to_craft, materials, recipes, inv):
    """
        Determine if a list of recipes can be crafted
        Inputs: toCraft=list(str), materials=dict, recipes=dict, inv=dict
        Returns: bool
    """
    # Setup Inventory
    inventory = [None] * inv["slots"]
    for material, info in materials.items():
        # Until material is empty
        while True:
            idx = inventory.index(None)
            mat_type = info["type"]
            mat_quantity = info["quantity"]
            slot = {
                "material": material,
                "quantity": inv[mat_type] if mat_quantity > inv[mat_type] else mat_quantity
            }
            inventory[idx] = slot
            info["quantity"] -= slot["quantity"]
            if info["quantity"] == 0:
                break
    try:
        for recipe in to_craft:
            # Add crafted item
            r_index = inventory.index(None)
            inventory[r_index] = {"material": recipe, "quantity": 1}
            # Remove Resources
            for rsc_name, rsc_needed, _, _ in recipes[recipe][2]:
                rsc_removed = 0
                while rsc_removed < rsc_needed:
                    rsc_still_needed = rsc_needed - rsc_removed
                    # Find resource index
                    rsc_index = [None if i is None else i["material"] for i in inventory].index(rsc_name)
                    if inventory[rsc_index]["quantity"] > rsc_still_needed:
                        # Remove whats needed
                        rsc_removed += rsc_still_needed
                        inventory[rsc_index]["quantity"] -= rsc_still_needed
                    elif rsc_still_needed >= inventory[rsc_index]["quantity"]:
                        # Remove all from inventory index
                        rsc_removed += inventory[rsc_index]["quantity"]
                        inventory[rsc_index] = None
        return True
    except Exception:
        return False
