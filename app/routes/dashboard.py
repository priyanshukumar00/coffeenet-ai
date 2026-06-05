from fastapi import APIRouter, Depends
from app.database.mongodb import database
from bson import ObjectId
from app.Utils.auth import manager_or_admin_required as manager_or_admin

router = APIRouter()

menu_collection = database["menu"]
order_collection = database["orders"]
inventory_collection = database["inventory"]

@router.get("/dashboard")
def get_dashboard(current_user = Depends(manager_or_admin)):

    total_products = menu_collection.count_documents({})

    total_orders = order_collection.count_documents({})

    pending_orders = order_collection.count_documents(
        {"status": "Pending"}
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
    
    low_stock_items = []
    low_stock_products = []
    for item in inventory_collection.find():

        if item["quantity"] <= item["minimum_stock"]:

            low_stock_items.append(item)

            low_stock_products.append(
                item["item_name"]
            )
    
    preparing_orders = order_collection.count_documents(
        {"status": "Preparing"}
    )
    ready_orders = order_collection.count_documents(
        {"status": "Ready"}
    )
    delivered_orders = order_collection.count_documents(
        {"status": "Delivered"}
    )
    cancelled_orders = order_collection.count_documents(
        {"status": "Cancelled"}
    )


    product_sales = {}

    for order in order_collection.find():

        for item in order["items"]:

            menu_item = menu_collection.find_one(
                {
                    "_id": ObjectId(item["menu_id"])
                }
            )

            if menu_item:

                product_name = menu_item["name"]

                if product_name not in product_sales:

                    product_sales[product_name] = 0

                product_sales[product_name] += item["quantity"]

    top_selling_products = sorted(
    product_sales.items(),
    key=lambda x: x[1],
    reverse=True)

    formatted_top_products = []
    for name, quantity in top_selling_products[:5]:

        formatted_top_products.append(
            {
                "product_name": name,
                "quantity_sold": quantity
            }
        )

         
    return {
    "total_products": total_products,
    "total_orders": total_orders,

    "pending_orders": pending_orders,
    "preparing_orders": preparing_orders,
    "ready_orders": ready_orders,
    "delivered_orders": delivered_orders,
    "cancelled_orders": cancelled_orders,

    "revenue": revenue,

    "low_stock_count": len(low_stock_items),
    "low_stock_products": low_stock_products,
    "top_selling_products": formatted_top_products
    }



