from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.menu import router as menu_router


app = FastAPI()
app.include_router(health_router)
app.include_router(menu_router)


@app.get("/")
def home():
    return{"message":"HELLO DEAR....Welcome to the coffeenet AI Platform"}


