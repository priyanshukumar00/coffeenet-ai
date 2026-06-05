from fastapi import APIRouter, Body, Depends
from bson import ObjectId
from app.schemas.order import Order
from app.database.mongodb import database
from app.schemas.order import OrderStatusUpdate
from bson.errors import InvalidId
from bson import ObjectId
from typing import Optional
from app.Utils.auth import cashier_or_admin_required as cashier_or_admin
from app.Utils.auth import kitchen_or_admin_required as kitchen_or_admin
from app.Utils.auth import manager_or_admin_required as manager_or_admin


router = APIRouter()
menu_collection = database["menu"]
order_collection = database["orders"]
recipe_collection = database["recipes"]
inventory_collection = database["inventory"]


@router.post("/orders")
def create_order(order: Order, current_user = Depends(cashier_or_admin)):

    total_amount = 0

    stock_deductions = []

    # -----------------------------
    # PASS 1 : VALIDATIONS
    # -----------------------------
    for item in order.items:

        if not ObjectId.is_valid(item.menu_id):

            return {
                "message":
                f"{item.menu_id} is not a valid menu id"
            }

        menu_item = menu_collection.find_one(
            {
                "_id": ObjectId(item.menu_id)
            }
        )

        if not menu_item:

            return {
                "message":
                f"Menu item {item.menu_id} not found"
            }

        total_amount += (
            menu_item["price"]
            * item.quantity
        )

        recipe = recipe_collection.find_one(
            {
                "menu_id": item.menu_id
            }
        )

        if not recipe:
            return {
                "message":
                f"No recipe found for menu item {item.menu_id}"
            }

        for ingredient in recipe["ingredients"]:

            inventory_item = inventory_collection.find_one(
                {
                    "_id": ObjectId(
                        ingredient["ingredient_id"]
                    )
                }
            )

            if not inventory_item:
                return {
                    "message":
                    f"Inventory item {ingredient['ingredient_id']} not found"
                }

            required_quantity = (
                ingredient["quantity"]
                * item.quantity
            )

            if inventory_item["quantity"] < required_quantity:

                return {
                    "message":
                    f"Insufficient stock for {inventory_item['item_name']}"
                }

            stock_deductions.append({
                "ingredient_id":
                ingredient["ingredient_id"],
                "required_quantity":
                required_quantity
            })

    # -----------------------------
    # PASS 2 : DEDUCT INVENTORY
    # -----------------------------
    for deduction in stock_deductions:

        inventory_collection.update_one(
            {
                "_id": ObjectId(
                    deduction["ingredient_id"]
                )
            },
            {
                "$inc": {
                    "quantity":
                    -deduction["required_quantity"]
                }
            }
        )

    # -----------------------------
    # PASS 3 : CREATE ORDER
    # -----------------------------
    order_data = {
        "items": order.model_dump(),
        "total_amount": total_amount,
        "status": "pending"
    }

    result = order_collection.insert_one(
        order_data
    )

    return {
        "message": "Order created successfully",
        "order_id": str(
            result.inserted_id
        ),
        "total_amount": total_amount
    }


@router.get("/orders")
def get_orders(
    page: int = 1,
    limit: int = 10,
    status: Optional[str] = None
):

    if page < 1:

        return {
            "message":
            "Page must be greater than 0"
        }

    if limit < 1 or limit > 100:

        return {
            "message":
            "Limit must be between 1 and 100"
        }

    query = {}

    valid_statuses = [
    "Pending",
    "Preparing",
    "Ready",
    "Delivered",
    "Cancelled"
]

    if status:

        if status not in valid_statuses:

            return {
                "message":
                "Invalid status"
            }

        query["status"] = status

    skip = (page - 1) * limit

    orders = []

    for order in order_collection.find(query)\
        .skip(skip)\
        .limit(limit):

        order["_id"] = str(order["_id"])

        orders.append(order)

    total_orders = order_collection.count_documents(
        query
    )

    return {
        "page": page,
        "limit": limit,
        "total_orders": total_orders,
        "orders": orders
    }


@router.get("/orders/{order_id}")
def get_order(order_id: str):

    if not ObjectId.is_valid(order_id):

        return {
            "message":
            "Invalid order id"
        }

    order = order_collection.find_one(
        {
            "_id": ObjectId(order_id)
        }
    )

    if not order:

        return {
            "message":
            "Order not found"
        }

    order["_id"] = str(order["_id"])

    return order



@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
    current_user = Depends(kitchen_or_admin)
):

    if not ObjectId.is_valid(order_id):

        return {
            "message":
            "Invalid order id"
        }

    order = order_collection.find_one(
        {
            "_id": ObjectId(order_id)
        }
    )

    if not order:

        return {
            "message":
            "Order not found"
        }

    current_status = order["status"]
    new_status = data.status.value

    valid_transitions = {
        "Pending": ["Preparing", "Cancelled"],
        "Preparing": ["Ready", "Cancelled"],
        "Ready": ["Delivered"],
        "Delivered": [],
        "Cancelled": []
    }

    if new_status not in valid_transitions[current_status]:

        return {
            "message":
            f"Cannot change status from {current_status} to {new_status}"
        }

    order_collection.update_one(
        {
            "_id": ObjectId(order_id)
        },
        {
            "$set": {
                "status": new_status
            }
        }
    )

    return {
        "message":
        f"Order status updated to {new_status}"
    }

@router.delete("/orders/{order_id}")
def delete_order(order_id: str, current_user = Depends(manager_or_admin)):

    if not ObjectId.is_valid(order_id):

        return {
            "message":
            "Invalid order id"
        }

    existing_order = order_collection.find_one(
        {
            "_id": ObjectId(order_id)
        }
    )

    if not existing_order:

        return {
            "message":
            "Order not found"
        }

    order_collection.delete_one(
        {
            "_id": ObjectId(order_id)
        }
    )

    return {
        "message":
        "Order deleted successfully"
    }

@router.delete("/orders")
def delete_orders(ids: list[str] = Body(...), current_user = Depends(manager_or_admin)):

    if not ids:

        return {
            "message":
            "Please provide at least one order id"
        }

    object_ids = []

    for order_id in ids:

        if not ObjectId.is_valid(order_id):

            return {
                "message":
                f"{order_id} is not a valid order id"
            }

        object_ids.append(
            ObjectId(order_id)
        )

    existing_count = order_collection.count_documents(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    if existing_count == 0:

        return {
            "message":
            "No matching orders found"
        }

    result = order_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message":
        f"{result.deleted_count} order(s) deleted successfully"
    }