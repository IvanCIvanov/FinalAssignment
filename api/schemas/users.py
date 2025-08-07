from typing import Optional
from pydantic import BaseModel
from .orders import Order
from .payments import Payment


class UserBase(BaseModel):
    customer_name: str
    rating: Optional[int] = None
    review: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_id: Optional[int] = None
    rating: Optional[int] = None
    review: Optional[str] = None


class User(UserBase):
    customer_id: int
    customer_name: str
    rating: Optional[int] = None
    review: Optional[str] = None
    order_id: Optional[int] = None

    class ConfigDict:
        from_attributes = True