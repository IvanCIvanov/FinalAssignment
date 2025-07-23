from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class User(Base):
    __tablename__ = "users"

    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))

    order = relationship("Order", back_populates="user")
    payment = relationship("Payment", back_populates="user")

    rating = Column(Integer, nullable = True)
    review = Column(String(500), nullable = True)