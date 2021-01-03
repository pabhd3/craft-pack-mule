# Pip Imports
from math import ceil, floor

# Script Imports
from methods import gatherNRecipes, gatherMaterials

# Asset Imports
from recipes import RECIPES

def scoreRecipes(toScore):
    """
    Apply a weighted score to each recipe based on minimum slots/caps needed
    Input: toScore=list(str)
    Returns: list(str)
    """
    # Constants
    BASE_CAPS = [10, 50, 100, 250, 500, 1000]
    MULTIPLIERS = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
    TYPES = [ "material", "mining", "fish", "food", "choppin", 
            "bug", "weapon", "armor", "tool", "bag", "inf" ]
    # Setup list of scored recipes
    SCORED = []
    # Setup Caps
    CAPS = [floor(m*b) for b in BASE_CAPS for m in MULTIPLIERS]
    # Loop though Recipes
    for r in toScore:
        # Starting recipe score
        rScore = 0
        # Check for nested recipes
        allRecipes = gatherNRecipes(toCraft=[r], recipes=RECIPES)
        # Gather materials
        typesNeeded = { k: False for k in TYPES }
        materials = gatherMaterials(toCraft=allRecipes, recipes=RECIPES)
        for mat, info in materials.items():
            typesNeeded[info["type"]] = True
            # Loop through CAPS
            matScore = 0
            for ci, c in enumerate(CAPS):
                # Check for max cap to make 1 slot
                slots = ceil(info["quantity"] / c)
                if(slots > 1):
                    matScore += (slots * ci)
            rScore += matScore
        # Apply number of cap types used
        rScore *= sum([1 for _,t in typesNeeded.items() if t])
        SCORED.append({"recipe": r, "score": rScore})
    return [rcp["recipe"] for rcp in sorted(SCORED, key=lambda r: r["score"])]
