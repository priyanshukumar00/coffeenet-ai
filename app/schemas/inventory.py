from pydantic import BaseModel, Field
from typing import Optional


class InventoryItem(BaseModel):

    item_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    quantity: float = Field(
        ...,
        ge=0
    )

    unit: str = Field(
        ...,
        min_length=1,
        max_length=20
    )

    minimum_stock: float = Field(
        ...,
        ge=0
    )


class InventoryItemUpdate(BaseModel):

    item_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )

    quantity: Optional[float] = Field(
        None,
        ge=0
    )

    unit: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20
    )

    minimum_stock: Optional[float] = Field(
        None,
        ge=0
    )