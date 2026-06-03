from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.menu import router as menu_router
from app.routes.order import router as order_router
from app.routes.dashboard import router as dashboard_router
from app.routes.inventory import router as inventory_router


app = FastAPI()
app.include_router(health_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(dashboard_router)
app.include_router(inventory_router)


@app.get("/")
def home():
    return{"message":"HELLO DEAR....Welcome to the coffeenet AI Platform"}
