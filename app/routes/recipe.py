from fastapi import APIRouter
from bson import ObjectId
from fastapi import Body

from app.database.mongodb import database
from app.schemas.recipe import Recipe

router = APIRouter()

recipe_collection = database["recipes"]


@router.post("/recipes")
def create_recipe(recipe: Recipe):

    recipe_dict = recipe.model_dump()

    result = recipe_collection.insert_one(
        recipe_dict
    )

    recipe_dict["_id"] = str(
        result.inserted_id
    )

    return {
        "message": "Recipe created successfully",
        "data": recipe_dict
    }



# ----- get all recipe -----
@router.get("/recipes")
def get_recipes():

    recipes = []

    for recipe in recipe_collection.find():

        recipe["_id"] = str(
            recipe["_id"]
        )

        recipes.append(recipe)

    return {
        "recipes": recipes
    }


#-----get single recipe --------
@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: str):

    recipe = recipe_collection.find_one(
        {"_id": ObjectId(recipe_id)}
    )

    if not recipe:

        return {
            "message": "Recipe not found"
        }

    recipe["_id"] = str(recipe["_id"])

    return recipe


# ----- update recipe --------------
@router.put("/recipes/{recipe_id}")
def update_recipe(
    recipe_id: str,
    recipe: Recipe
):

    updated_data = recipe.model_dump()

    recipe_collection.update_one(
        {"_id": ObjectId(recipe_id)},
        {"$set": updated_data}
    )

    return {
        "message": "Recipe updated successfully"
    }


#------- Delete Multiple Recipe ---------
@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: str):

    recipe_collection.delete_one(
        {"_id": ObjectId(recipe_id)}
    )

    return {
        "message": "Recipe deleted successfully"
    }



#delete multiple Recipes --------
@router.delete("/recipes")
def delete_recipes(ids: list[str] = Body(...)):

    object_ids = [
        ObjectId(id)
        for id in ids
    ]

    result = recipe_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message":
        f"{result.deleted_count} recipe(s) deleted"
    }


# ------- Find recipe by menu item -----------
@router.get("/recipes/menu/{menu_id}")
def get_recipe_by_menu(menu_id: str):

    recipe = recipe_collection.find_one(
        {"menu_id": menu_id}
    )

    if not recipe:

        return {
            "message": "Recipe not found"
        }

    recipe["_id"] = str(recipe["_id"])

    return recipe

