from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource
from .sandwiches import Sandwich


class RecipeBase(BaseModel):
    sandwich_id: int
    ingredient_id: int

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    ingredient_id: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    sandwich: Sandwich = None
    ingredient: Resource = None

    class ConfigDict:
        from_attributes = True