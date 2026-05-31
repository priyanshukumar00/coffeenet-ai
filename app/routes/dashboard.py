from fastapi import APIRouter
from app.database.mongodb import database

router = APIRouter()

menu_collection = database["menu"]
order_collection = database["orders"]