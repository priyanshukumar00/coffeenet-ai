from fastapi import APIRouter
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

