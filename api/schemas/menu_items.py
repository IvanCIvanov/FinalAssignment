from typing import Optional
from pydantic import BaseModel
from .recipes import Recipe
from datetime import datetime


class MenuItemBase(BaseModel):
    promotion_code: Optional[str] = None
    expiration_date: Optional[datetime] = None


class MenuItemCreate(MenuItemBase):
    recipe_id: int


class MenuItemUpdate(BaseModel):
    recipe_id: Optional[int] = None
    promotion_code: Optional[str] = None
    expiration_date: Optional[datetime] = None

class MenuItem(MenuItemBase):
    sandwich_id: int
    recipe: Recipe = None

    class ConfigDict:
        from_attributes = True