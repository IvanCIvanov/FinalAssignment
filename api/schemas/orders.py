from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderBase(BaseModel):
    user_id: int
    sandwich_id: int
    amount: int


class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    amount: Optional[int] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
