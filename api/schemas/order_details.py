from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .sandwiches import Sandwich


class OrderDetailBase(BaseModel):
    order_id: int
    amount: int
    sandwich_id: int


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    sandwich_id: int
    sandwich_name: Optional[str]

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    amount: Optional[int] = None
    sandwich_name: Optional[str] = None


class OrderDetail(OrderDetailBase):
    order_details_id: int
    sandwich_name: Optional[str] = str

    class ConfigDict:
        from_attributes = True
        allow_population_by_field_name = True