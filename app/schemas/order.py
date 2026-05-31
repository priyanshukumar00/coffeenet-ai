from pydantic import BaseModel
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    Pending = "Pending"
    Preparing = "Preparing"
    Ready = "Ready"
    Delivered = "Delivered"
    Cancelled = "Cancelled"


class OrderItem(BaseModel):
    menu_id: str
    quantity: int


class Order(BaseModel):
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.Pending


class OrderStatusUpdate(BaseModel):
    status: OrderStatus