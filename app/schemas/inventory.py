from pydantic import BaseModel
from typing import Optional


class InventoryItem(BaseModel):
    item_name: str
    quantity: float
    unit: str
    minimum_stock: float


class InventoryItemUpdate(BaseModel):
    item_name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    minimum_stock: Optional[float] = None