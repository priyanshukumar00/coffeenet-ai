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

    return {
        "total_amount": total_amount
    }