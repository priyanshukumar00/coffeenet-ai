from fastapi import APIRouter
from bson import ObjectId
from app.schemas.order import Order
from app.database.mongodb import database

router = APIRouter()
menu_collection = database["menu"]
order_collection = database["orders"]


@router.post("/orders")
def create_order(order: Order):

    total_amount = 0

    for item in order.items:

        menu_item = menu_collection.find_one(
            {"_id": ObjectId(item.menu_id)}
        )

        total_amount += menu_item["price"] * item.quantity

    order_data = {
        "items": order.model_dump(),
        "total_amount": total_amount,
        "status": "pending"
    }

    result = order_collection.insert_one(order_data)

    return {
        "message": "Order created successfully",
        "order_id": str(result.inserted_id),
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
