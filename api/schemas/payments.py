from typing import Optional
from pydantic import BaseModel
from .orders import Order

class PaymentBase(BaseModel):
    payment_type: str
    order_id: int

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    payment_type: Optional[str] = None
    customer_id: Optional[int] = None
    order_id: Optional[int] = None

class Payment(PaymentBase):
    id: int
    order: Order = None

    class Config:
        from_attributes = True

