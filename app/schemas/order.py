from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    menu_id: str
    quantity: int

class Order(BaseModel):
    items: List[OrderItem]