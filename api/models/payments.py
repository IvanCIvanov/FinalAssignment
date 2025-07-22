from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.customers_id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    payment_type = Column(String(100))

    user = relationship("User", back_populates="payment")
    order = relationship("Order", back_populates="payment")