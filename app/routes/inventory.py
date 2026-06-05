from fastapi import APIRouter, Body, Depends
from bson import ObjectId
from fastapi import Query

from app.database.mongodb import database
from app.schemas.inventory import InventoryItem
from app.schemas.inventory import InventoryItemUpdate
from app.Utils.auth import manager_or_admin_required as manager_or_admin

router = APIRouter()

inventory_collection = database["inventory"]
recipe_collection = database["recipes"]


@router.post("/inventory")
def create_inventory_item(item: InventoryItem, current_user = Depends(manager_or_admin)):

    existing_item = inventory_collection.find_one(
        {
            "item_name": {
                "$regex": f"^{item.item_name}$",
                "$options": "i"
            }
        }
    )

    if existing_item:

        return {
            "message": f"{item.item_name} already exists in inventory"
        }

    item_dict = item.model_dump()

    result = inventory_collection.insert_one(item_dict)

    item_dict["_id"] = str(result.inserted_id)

    return {
        "message": "Inventory item added successfully",
        "data": item_dict
    }


@router.get("/inventory")
def get_inventory(

    search: str = Query(
        default=None
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    )

):

    query = {}

    if search:

        query["item_name"] = {
            "$regex": search,
            "$options": "i"
        }

    skip = (page - 1) * limit

    items = []

    cursor = (
        inventory_collection
        .find(query)
        .skip(skip)
        .limit(limit)
    )

    for item in cursor:

        item["_id"] = str(item["_id"])

        items.append(item)

    total_items = inventory_collection.count_documents(
        query
    )

    return {

        "page": page,

        "limit": limit,

        "total_items": total_items,

        "inventory": items
    }

@router.put("/inventory/{item_id}")
def update_inventory_item(
    item_id: str,
    item: InventoryItemUpdate,
    current_user = Depends(manager_or_admin)
):

    if not ObjectId.is_valid(item_id):

        return {
            "message":
            "Invalid inventory item id"
        }

    existing_item = inventory_collection.find_one(
        {
            "_id": ObjectId(item_id)
        }
    )

    if not existing_item:

        return {
            "message":
            "Inventory item not found"
        }

    update_data = item.model_dump(
        exclude_unset=True
    )

    if not update_data:

        return {
            "message":
            "No data provided for update"
        }

    if "item_name" in update_data:

        duplicate_item = inventory_collection.find_one(
            {
                "item_name": {
                    "$regex":
                    f"^{update_data['item_name']}$",
                    "$options": "i"
                },
                "_id": {
                    "$ne": ObjectId(item_id)
                }
            }
        )

        if duplicate_item:

            return {
                "message":
                f"{update_data['item_name']} already exists"
            }

    inventory_collection.update_one(
        {
            "_id": ObjectId(item_id)
        },
        {
            "$set": update_data
        }
    )

    return {
        "message":
        "Inventory item updated successfully"
    }


@router.delete("/inventory")
def delete_inventory_items(
    ids: list[str] = Body(...), 
    current_user = Depends(manager_or_admin)
):

    if not ids:

        return {
            "message":
            "Please provide at least one inventory id"
        }

    object_ids = []

    for item_id in ids:

        if not ObjectId.is_valid(item_id):

            return {
                "message":
                f"{item_id} is not a valid inventory id"
            }

        recipe_exists = recipe_collection.find_one(
            {
                "ingredients.ingredient_id": item_id
            }
        )

        if recipe_exists:

            return {
                "message":
                "Cannot delete inventory item because it is being used in a recipe"
            }

        object_ids.append(
            ObjectId(item_id)
        )

    result = inventory_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message":
        f"{result.deleted_count} inventory item(s) deleted successfully"
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
