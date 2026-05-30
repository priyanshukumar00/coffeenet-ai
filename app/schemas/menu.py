from pydantic import BaseModel
from typing import Optional

class MenuItem(BaseModel):
    name: str
    price: float
    category: str
    description: str


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None