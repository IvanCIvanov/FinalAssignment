from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    ingredient_name: str
    amount: int


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    ingredient_name: Optional[str] = None
    amount: Optional[int] = None


class Resource(ResourceBase):
    ingredient_name: str
    amount: int

    class ConfigDict:
        from_attributes = True
