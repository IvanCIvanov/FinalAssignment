from typing import Optional
from pydantic import BaseModel
from .orders import Order


class PaymentBase(BaseModel):
    payment_type: str


class PaymentCreate(PaymentBase):
    customer_id: int
    order_id: int


class PaymentUpdate(BaseModel):
    payment_type: Optional[str] = None
    customer_id: Optional[int] = None
    order_id: Optional[int] = None


class Payment(PaymentBase):
    id: int
    user: "User" = None
    order: Order = None

    class ConfigDict:
        from_attributes = True

from users import User