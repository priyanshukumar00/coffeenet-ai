from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import router as health_router
from app.routes.menu import router as menu_router
from app.routes.order import router as order_router
from app.routes.dashboard import router as dashboard_router
from app.routes.inventory import router as inventory_router
from app.routes.recipe import router as recipe_router
from app.routes.user import router as user_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#routes
app.include_router(health_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(dashboard_router)
app.include_router(inventory_router)
app.include_router(recipe_router)
app.include_router(user_router)


#home
@app.get("/")
def home():
    return{"message":"BrewGO.. Coffee on the go"}
