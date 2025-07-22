from typing import Optional
from pydantic import BaseModel
from .orders import Order
from .payments import Payment


class UserBase(BaseModel):
    pass  # No shared fields yet


class UserCreate(UserBase):
    order_id: int


class UserUpdate(BaseModel):
    order_id: Optional[int] = None


class User(UserBase):
    customer_id: int
    order: Optional[Order] = None
    payment: Optional[list[Payment]] = None

    class ConfigDict:
        from_attributes = True