from pydantic import BaseModel, Field
from typing import List


class RecipeIngredient(BaseModel):

    ingredient_id: str = Field(
        ...,
        min_length=24,
        max_length=24
    )

    quantity: float = Field(
        ...,
        gt=0
    )


class Recipe(BaseModel):

    menu_id: str = Field(
        ...,
        min_length=24,
        max_length=24
    )

    ingredients: List[RecipeIngredient] = Field(
        ...,
        min_length=1
    )