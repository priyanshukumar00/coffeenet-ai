from pydantic import BaseModel, Field
from typing import Optional


class MenuItem(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    price: float = Field(
        ...,
        gt=0
    )

    category: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=500
    )


class MenuItemUpdate(BaseModel):

    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )

    price: Optional[float] = Field(
        None,
        gt=0
    )

    category: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50
    )

    description: Optional[str] = Field(
        None,
        min_length=5,
        max_length=500
    )