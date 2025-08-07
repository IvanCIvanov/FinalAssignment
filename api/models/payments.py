from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.customer_id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_type = Column(String(100))
    payment_date = Column(DATETIME, default=datetime.utcnow)
    amount_paid = Column(DECIMAL(10,2), nullable=False)

    user = relationship("User", back_populates="payment")
    order = relationship("Order", back_populates="payment")