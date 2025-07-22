from typing import Optional
from pydantic import BaseModel
from .recipes import Recipe



class MenuItemBase(BaseModel):
    pass


class MenuItemCreate(MenuItemBase):
    recipe_id: int


class MenuItemUpdate(BaseModel):
    recipe_id: Optional[int] = None


class MenuItem(MenuItemBase):
    sandwich_id: int
    recipe: Recipe = None

    class ConfigDict:
        from_attributes = True