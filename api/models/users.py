from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class User(Base):
    __tablename__ = "users"

    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Integer, nullable=True)
    review = Column(String(500), nullable=True)



    # Relationships
    orders = relationship("Order", back_populates="user")
    payment = relationship("Payment", back_populates="user")