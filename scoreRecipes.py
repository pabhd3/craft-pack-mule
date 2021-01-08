# Pip Imports
from math import ceil, floor

# Script Imports
from methods import gatherNRecipes, gatherMaterials

# Asset Imports
from recipes import MATERIAL_WEIGHTS, RECIPES


def scoreRecipes(toCraft):
    # Constants
    BASE_CAPS = [10, 50, 100, 250, 500, 1000]
    MULTIPLIERS = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
    TYPES = [ "material", "mining", "fish", "food", "choppin", 
            "bug", "weapon", "armor", "tool", "bag", "inf" ]
    # Setup list of scored recipes
    SCORED = []
    # Setup Caps
    CAPS = [floor(m*b) for b in BASE_CAPS for m in MULTIPLIERS]
    for r in toCraft:
        # Setup score by capacity & material
        capScore, wgtScore = 0, 0
        # Check for nested recipes
        allRecipes = gatherNRecipes(toCraft=[r], recipes=RECIPES)
        # Gather materials
        typesNeeded = { k: False for k in TYPES }
        materials = gatherMaterials(toCraft=allRecipes, recipes=RECIPES)
        for mat, info in materials.items():
            # Mark type as needed
            typesNeeded[info["type"]] = True
            # Find material's score by weight
            matWgtScore = 1
            for mwi, matWeights in enumerate(MATERIAL_WEIGHTS):
                if(mat in matWeights):
                    matWgtScore = mwi
            wgtScore += matWgtScore
            # Find material's score by cap
            matCapScore = 1
            for capI, cap in enumerate(CAPS):
                slots = ceil(info["quantity"] / cap)
                if(slots > 1):
                    matCapScore += (slots * capI)
            capScore += matCapScore
        SCORED.append({"name": r, "weight": wgtScore, "cap": capScore})
    # Find rank based on Weight and Cap
    CAP_SCORE = [r["name"] for r in sorted(SCORED, key=lambda c: c["cap"])]
    WEIGHT_SCORE = [r["name"] for r in sorted(SCORED, key=lambda w: w["weight"])]
    # Find new new score based on cap:weight
    nScores = len(SCORED)
    for sr in SCORED:
        # Find respective indices
        capI = CAP_SCORE.index(sr["name"])
        wgtI = WEIGHT_SCORE.index(sr["name"])
        # Apply ratio
        rScore = ceil(wgtI * 0.7) + floor(capI * 0.3)
        sr["total"] = rScore
    return [r["name"] for r in sorted(SCORED, key=lambda x: x["total"])]
