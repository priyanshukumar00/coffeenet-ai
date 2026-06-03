from pydantic import BaseModel
from typing import List


class RecipeIngredient(BaseModel):
    ingredient_id: str
    quantity: float


class Recipe(BaseModel):
    menu_id: str
    ingredients: List[RecipeIngredient]
