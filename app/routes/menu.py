from fastapi import APIRouter
from bson import ObjectId
from app.schemas.menu import MenuItem
from app.schemas.menu import MenuItemUpdate
from app.database.mongodb import database
from fastapi import Body
from fastapi import Depends
from app.Utils.auth import admin_required as admin

router = APIRouter()

menu_collection = database["menu"]

@router.post("/menu")
def create_menu_item(item: MenuItem,current_user = Depends(admin)):

    existing_item = menu_collection.find_one(
        {
            "name": {
                "$regex": f"^{item.name}$",
                "$options": "i"
            }
        }
    )

    if existing_item:
        return {
            "message":
            f"{item.name} already exists in menu"
        }

    item_dict = item.model_dump()

    result = menu_collection.insert_one(
        item_dict
    )

    item_dict["_id"] = str(
        result.inserted_id
    )

    return {
        "message":
        "Menu item stored successfully",
        "data": item_dict
    }


@router.get("/menu")
def get_menu_items():

    items = []

    for item in menu_collection.find():

        item["_id"] = str(item["_id"])

        items.append(item)

    if not items:

        return {
            "message": "No menu items found",
            "menu": []
        }

    return {
        "menu": items
    }



@router.delete("/menu")
def delete_menu_items(ids: list[str] = Body(...), current_user = Depends(admin)):

    if not ids:

        return {
            "message": "Please provide at least one menu item id"
        }

    object_ids = []

    for item_id in ids:

        if not ObjectId.is_valid(item_id):

            return {
                "message": f"{item_id} is not a valid menu item id"
            }

        object_ids.append(
            ObjectId(item_id)
        )

    existing_count = menu_collection.count_documents(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    if existing_count == 0:

        return {
            "message": "No menu items found to delete"
        }

    result = menu_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message":
        f"{result.deleted_count} menu item(s) deleted successfully"
    }



@router.put("/menu/{item_id}")
def update_menu_item(item_id: str, item: MenuItemUpdate, current_user = Depends(admin)):

    if not ObjectId.is_valid(item_id):

        return {
            "message": "Invalid menu item id"
        }

    existing_item = menu_collection.find_one(
        {
            "_id": ObjectId(item_id)
        }
    )

    if not existing_item:

        return {
            "message": "Menu item not found"
        }

    update_data = item.model_dump(
        exclude_unset=True
    )

    if not update_data:

        return {
            "message": "No data provided for update"
        }

    menu_collection.update_one(
        {
            "_id": ObjectId(item_id)
        },
        {
            "$set": update_data
        }
    )

    return {
        "message": "Menu item updated successfully"
    }
    

@router.patch("/menu/{item_id}")
def update_menu_item(
    item_id: str,
    item: MenuItemUpdate,
    current_user = Depends(admin)
):

    if not ObjectId.is_valid(item_id):

        return {
            "message": "Invalid menu item id"
        }

    existing_item = menu_collection.find_one(
        {
            "_id": ObjectId(item_id)
        }
    )

    if not existing_item:

        return {
            "message": "Menu item not found"
        }

    update_data = item.model_dump(
        exclude_unset=True
    )

    if not update_data:

        return {
            "message": "No data provided for update"
        }

    menu_collection.update_one(
        {
            "_id": ObjectId(item_id)
        },
        {
            "$set": update_data
        }
    )

    return {
        "message": "Menu item updated successfully"
    }

@router.get("/menu/{item_id}")
def get_menu_item(item_id: str):

    if not ObjectId.is_valid(item_id):

        return {
            "message": "Invalid menu item id"
        }

    item = menu_collection.find_one(
        {
            "_id": ObjectId(item_id)
        }
    )

    if not item:

        return {
            "message": "Menu item not found"
        }

    item["_id"] = str(item["_id"])

    return {
        "message": "Menu item fetched successfully",
        "data": item
    }