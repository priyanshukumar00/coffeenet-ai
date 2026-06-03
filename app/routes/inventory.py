from fastapi import APIRouter
from bson import ObjectId

from app.database.mongodb import database
from app.schemas.inventory import InventoryItem
from app.schemas.inventory import InventoryItemUpdate

router = APIRouter()

inventory_collection = database["inventory"]


@router.post("/inventory")
def create_inventory_item(item: InventoryItem):

    item_dict = item.model_dump()

    result = inventory_collection.insert_one(item_dict)

    item_dict["_id"] = str(result.inserted_id)

    return {
        "message": "Inventory item added successfully",
        "data": item_dict
    }

@router.get("/inventory")
def get_inventory():

    items = []

    for item in inventory_collection.find():

        item["_id"] = str(item["_id"])

        items.append(item)

    return {
        "inventory": items
    }

@router.put("/inventory/{item_id}")
def update_inventory_item(item_id: str, item: InventoryItemUpdate):

    update_data = item.model_dump(exclude_unset=True)

    result = inventory_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": update_data}
    )

    return {
        "message": "Inventory item updated successfully"
    }


@router.delete("/inventory")
def delete_inventory_items(ids: list[str]):

    object_ids = [ObjectId(id) for id in ids]

    result = inventory_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message": f"{result.deleted_count} inventory item(s) deleted successfully"
    }


@router.get("/inventory/low-stock")
def get_low_stock_items():

    items = []

    for item in inventory_collection.find():

        if item["quantity"] <= item["minimum_stock"]:

            item["_id"] = str(item["_id"])

            items.append(item)

    return {
        "low_stock_items": items
    }

#-----Total Count of Inventory Items ---------
@router.get("/inventory/count")
def inventory_count():

    count = inventory_collection.count_documents({})

    return {
        "total_inventory_items": count
    }

# ----- low stock count ------
@router.get("/inventory/low-stock/count")
def low_stock_count():

    count = 0

    for item in inventory_collection.find():

        if item["quantity"] <= item["minimum_stock"]:

            count += 1

    return {
        "low_stock_count": count
    }

#-----Total Avaialable Quantity --------
@router.get("/inventory/quantity")
def total_inventory_quantity():

    total_quantity = 0

    for item in inventory_collection.find():

        total_quantity += item["quantity"]

    return {
        "total_quantity": total_quantity
    }


#------- Inventory Summary API ---------
@router.get("/inventory/dashboard")
def inventory_dashboard():

    total_items = inventory_collection.count_documents({})

    low_stock = 0

    total_quantity = 0

    for item in inventory_collection.find():

        total_quantity += item["quantity"]

        if item["quantity"] <= item["minimum_stock"]:

            low_stock += 1

    return {
        "total_inventory_items": total_items,
        "low_stock_items": low_stock,
        "total_quantity": total_quantity
    }
