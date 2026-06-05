from fastapi import APIRouter, Depends
from bson import ObjectId
from fastapi import Body

from app.database.mongodb import database
from app.schemas.recipe import Recipe
from app.Utils.auth import manager_or_admin_required as manager_or_admin

router = APIRouter()

recipe_collection = database["recipes"]
menu_collection = database["menu"]
inventory_collection = database["inventory"]


@router.post("/recipes")
def create_recipe(recipe: Recipe, current_user = Depends(manager_or_admin)):

    if not ObjectId.is_valid(recipe.menu_id):

        return {
            "message":
            "Invalid menu id"
        }

    menu_item = menu_collection.find_one(
        {
            "_id": ObjectId(recipe.menu_id)
        }
    )

    if not menu_item:

        return {
            "message":
            "Menu item not found"
        }

    existing_recipe = recipe_collection.find_one(
        {
            "menu_id": recipe.menu_id
        }
    )

    if existing_recipe:

        return {
            "message":
            "Recipe already exists for this menu item"
        }

    ingredient_ids = []

    for ingredient in recipe.ingredients:

        if not ObjectId.is_valid(
            ingredient.ingredient_id
        ):

            return {
                "message":
                f"{ingredient.ingredient_id} is not a valid ingredient id"
            }

        inventory_item = inventory_collection.find_one(
            {
                "_id": ObjectId(
                    ingredient.ingredient_id
                )
            }
        )

        if not inventory_item:

            return {
                "message":
                "Inventory item not found"
            }

        if ingredient.ingredient_id in ingredient_ids:

            return {
                "message":
                "Duplicate ingredient found in recipe"
            }

        ingredient_ids.append(
            ingredient.ingredient_id
        )

    recipe_dict = recipe.model_dump()

    result = recipe_collection.insert_one(
        recipe_dict
    )

    recipe_dict["_id"] = str(
        result.inserted_id
    )

    return {
        "message":
        "Recipe created successfully",
        "data":
        recipe_dict
    }


@router.put("/recipes/{recipe_id}")
def update_recipe(
    recipe_id: str,
    recipe: Recipe,
    current_user = Depends(manager_or_admin)
):

    if not ObjectId.is_valid(recipe_id):

        return {
            "message":
            "Invalid recipe id"
        }

    existing_recipe = recipe_collection.find_one(
        {
            "_id": ObjectId(recipe_id)
        }
    )

    if not existing_recipe:

        return {
            "message":
            "Recipe not found"
        }

    if not ObjectId.is_valid(recipe.menu_id):

        return {
            "message":
            "Invalid menu id"
        }

    menu_item = menu_collection.find_one(
        {
            "_id": ObjectId(recipe.menu_id)
        }
    )

    if not menu_item:

        return {
            "message":
            "Menu item not found"
        }

    duplicate_recipe = recipe_collection.find_one(
        {
            "menu_id": recipe.menu_id,
            "_id": {
                "$ne": ObjectId(recipe_id)
            }
        }
    )

    if duplicate_recipe:

        return {
            "message":
            "Another recipe already exists for this menu item"
        }

    ingredient_ids = []

    for ingredient in recipe.ingredients:

        if not ObjectId.is_valid(
            ingredient.ingredient_id
        ):

            return {
                "message":
                f"{ingredient.ingredient_id} is not a valid ingredient id"
            }

        inventory_item = inventory_collection.find_one(
            {
                "_id": ObjectId(
                    ingredient.ingredient_id
                )
            }
        )

        if not inventory_item:

            return {
                "message":
                "Inventory item not found"
            }

        if ingredient.ingredient_id in ingredient_ids:

            return {
                "message":
                "Duplicate ingredient found in recipe"
            }

        ingredient_ids.append(
            ingredient.ingredient_id
        )

    updated_data = recipe.model_dump()

    recipe_collection.update_one(
        {
            "_id": ObjectId(recipe_id)
        },
        {
            "$set": updated_data
        }
    )

    return {
        "message":
        "Recipe updated successfully"
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



# ----- get recipe --------------
@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: str):

    if not ObjectId.is_valid(recipe_id):

        return {
            "message":
            "Invalid recipe id"
        }

    recipe = recipe_collection.find_one(
        {
            "_id": ObjectId(recipe_id)
        }
    )

    if not recipe:

        return {
            "message":
            "Recipe not found"
        }

    recipe["_id"] = str(
        recipe["_id"]
    )

    return recipe


#------- Delete Single Recipe ---------
@router.delete("/recipes/{recipe_id}")
def delete_recipe(
    recipe_id: str, 
    current_user = Depends(manager_or_admin)
    ):

    if not ObjectId.is_valid(recipe_id):

        return {
            "message":
            "Invalid recipe id"
        }

    existing_recipe = recipe_collection.find_one(
        {
            "_id": ObjectId(recipe_id)
        }
    )

    if not existing_recipe:

        return {
            "message":
            "Recipe not found"
        }

    result = recipe_collection.delete_one(
        {
            "_id": ObjectId(recipe_id)
        }
    )

    return {
        "message":
        "Recipe deleted successfully"
    }



#delete multiple Recipes --------
@router.delete("/recipes")
def delete_recipes(ids: list[str] = Body(...),current_user = Depends(manager_or_admin)):

    if not ids:

        return {
            "message":
            "Please provide at least one recipe id"
        }

    object_ids = []

    for recipe_id in ids:

        if not ObjectId.is_valid(recipe_id):

            return {
                "message":
                f"{recipe_id} is not a valid recipe id"
            }

        object_ids.append(
            ObjectId(recipe_id)
        )

    existing_count = recipe_collection.count_documents(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    if existing_count == 0:

        return {
            "message":
            "No matching recipes found"
        }

    result = recipe_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message":
        f"{result.deleted_count} recipe(s) deleted successfully"
    }


# ------- Find recipe by menu item -----------
@router.get("/recipes/menu/{menu_id}")
def get_recipe_by_menu(menu_id: str):

    if not ObjectId.is_valid(menu_id):

        return {
            "message":
            "Invalid menu id"
        }

    menu_item = menu_collection.find_one(
        {
            "_id": ObjectId(menu_id)
        }
    )

    if not menu_item:

        return {
            "message":
            "Menu item not found"
        }

    recipe = recipe_collection.find_one(
        {
            "menu_id": menu_id
        }
    )

    if not recipe:

        return {
            "message":
            "Recipe not found"
        }

    recipe["_id"] = str(
        recipe["_id"]
    )
    return recipe

