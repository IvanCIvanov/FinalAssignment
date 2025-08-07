from typing import Optional
from pydantic import BaseModel, Field
from .orders import Order
from datetime import date

class PaymentBase(BaseModel):
    payment_type: str
    order_id: int
    customer_id: int
    payment_date: date = Field(default_factory=date.today)
    amount_paid: float

class PaymentCreate(PaymentBase):
    id: int
    payment_type: str
    order_id: int
    customer_id: int
    payment_date: date = Field(default_factory=date.today)
    amount_paid: float

class PaymentUpdate(BaseModel):
    payment_type: Optional[str] = None
    customer_id: Optional[int] = None
    order_id: Optional[int] = None

class Payment(PaymentBase):
    id: int
    order: Order = None

    class Config:
        from_attributes = True

