from fastapi import APIRouter
from app.database.mongodb import database
from bson import ObjectId

router = APIRouter()

menu_collection = database["menu"]
order_collection = database["orders"]
inventory_collection = database["inventory"]

@router.get("/dashboard")
def get_dashboard():

    total_products = menu_collection.count_documents({})

    total_orders = order_collection.count_documents({})

    pending_orders = order_collection.count_documents(
        {"status": "pending"}
    )

    revenue = 0

    for order in order_collection.find():

        for item in order["items"]:

            menu_item = menu_collection.find_one(
                {"_id": ObjectId(item["menu_id"])}
            )

            if menu_item:

                revenue += (
                    menu_item["price"]
                    * item["quantity"]
                )
    
    low_stock_items = list(
        inventory_collection.find(
        {"stock": {"$lt": 10}}))

    low_stock_products = []

    for item in low_stock_items:
        low_stock_products.append(item["product_name"])

    return {
    "total_products": total_products,
    "total_orders": total_orders,
    "pending_orders": pending_orders,
    "revenue": revenue,
    "low_stock_count": len(low_stock_items),
    "low_stock_products": low_stock_products
    }

