from fastapi import APIRouter
from bson import ObjectId
from app.schemas.menu import MenuItem
from app.schemas.menu import MenuItemUpdate
from app.database.mongodb import database
from fastapi import Body

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

@router.delete("/menu")
def delete_menu_items(ids: list[str] = Body(...)):

    object_ids = [ObjectId(id) for id in ids]

    result = menu_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message": f"{result.deleted_count} item(s) deleted successfully"
    }



@router.put("/menu/{item_id}")
def update_menu_item(item_id: str, item: MenuItemUpdate):

    update_data = item.model_dump(exclude_unset=True)

    result = menu_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": update_data}
    )

    return {
        "message": "Menu item updated successfully"
    }
    

@router.patch("/menu/{item_id}")
def update_menu_item(item_id: str, updates: dict = Body(...)):

    result = menu_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": updates}
    )

    return {
        "message": "Menu item updated successfully"
    }