from typing import Optional
from pydantic import BaseModel
from .orders import Order
#from .payments import Payment


class UserBase(BaseModel):
    rating: Optional[int] = None
    review: Optional[str] = None
    payment: Optional[list["Payment"]] = None
    order: Optional[list[Order]] = None

class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    #order_id: Optional[int] = None
    rating: Optional[int] = None
    review: Optional[str] = None


class User(UserBase):
    customer_id: int
    #order: Optional[Order] = None
    #payment: Optional[list[Payment]] = None

    class ConfigDict:
        from_attributes = True