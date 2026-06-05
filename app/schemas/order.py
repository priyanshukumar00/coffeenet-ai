from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    Pending = "Pending"
    Preparing = "Preparing"
    Ready = "Ready"
    Delivered = "Delivered"
    Cancelled = "Cancelled"


class OrderItem(BaseModel):
    menu_id: str = Field(
        ...,
        min_length=24,
        max_length=24
    )

    quantity: int = Field(
        ...,
        gt=0
    )


class Order(BaseModel):
    items: List[OrderItem] = Field(
        ...,
        min_length=1
    )

    status: OrderStatus = OrderStatus.Pending


class OrderStatusUpdate(BaseModel):
    status: OrderStatus