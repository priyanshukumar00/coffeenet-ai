from fastapi import APIRouter
from bson import ObjectId
from app.schemas.menu import MenuItem
from app.database.mongodb import database

router = APIRouter()

menu_collection = database["menu"]

@router.post("/menu")
def create_menu_item(item: MenuItem):

    item_dict = item.model_dump()

    result = menu_collection.insert_one(item_dict)

    item_dict["_id"] = str(result.inserted_id)

    return {
        "message": "Menu item stored successfully",
        "data": item_dict
    }

@router.get("/menu")
def get_menu_items():

    items = []

    for item in menu_collection.find():

        item["_id"] = str(item["_id"])

        items.append(item)

    return {
        "menu": items
    }


@router.put("/menu/{item_id}")
def update_menu_item(item_id: str, item: MenuItem):

    updated_data = item.model_dump()

    result = menu_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": updated_data}
    )

    if result.modified_count == 1:

        return {
            "message": "Menu item updated successfully"
        }

    return {
        "message": "No item updated"
    }

@router.delete("/menu/{item_id}")
def delete_menu_item(item_id: str):

    result = menu_collection.delete_one(
        {"_id": ObjectId(item_id)}
    )

    if result.deleted_count == 1:

        return {
            "message": "Menu item deleted successfully"
        }

    return {
        "message": "No item found"
    }