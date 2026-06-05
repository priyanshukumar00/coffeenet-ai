from fastapi import APIRouter
from bson import ObjectId
from app.database.mongodb import database

router = APIRouter()

order_collection = database["orders"]
menu_collection = database["menu"]


@router.get("/reports")
def get_reports():

    total_orders = order_collection.count_documents({})

    total_revenue = 0

    for order in order_collection.find():

        total_revenue += order.get(
            "total_amount",
            0
        )

    average_order_value = 0

    if total_orders > 0:

        average_order_value = (
            total_revenue / total_orders
        )

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "average_order_value": round(
            average_order_value,
            2
        )
    }