from fastapi import APIRouter, Body
from bson import ObjectId
from app.schemas.order import Order
from app.database.mongodb import database
from app.schemas.order import OrderStatusUpdate
from bson.errors import InvalidId
from bson import ObjectId

router = APIRouter()
menu_collection = database["menu"]
order_collection = database["orders"]
recipe_collection = database["recipes"]
inventory_collection = database["inventory"]

@router.post("/orders")
def create_order(order: Order):

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
def get_orders():

    orders = []

    for order in order_collection.find():

        order["_id"] = str(order["_id"])

        orders.append(order)

    return {
        "orders": orders
    }


@router.get("/orders/{order_id}")
def get_order(order_id: str):

    order = order_collection.find_one(
        {"_id": ObjectId(order_id)}
    )

    if not order:
        return {
            "message": "Order not found"
        }

    order["_id"] = str(order["_id"])

    return order



@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: str,
    data: OrderStatusUpdate
):

    result = order_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": data.status}}
    )

    return {
        "message": "Order status updated successfully"
    }


@router.delete("/orders/{order_id}")
def delete_order(order_id: str):

    result = order_collection.delete_one(
        {"_id": ObjectId(order_id)}
    )

    return {
        "message": "Order deleted successfully"
    }

@router.delete("/orders")
def delete_orders(ids: list[str] = Body(...)):

    object_ids = [ObjectId(id) for id in ids]

    result = order_collection.delete_many(
        {
            "_id": {
                "$in": object_ids
            }
        }
    )

    return {
        "message": f"{result.deleted_count} order(s) deleted successfully"
    }