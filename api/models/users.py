from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class User(Base):
    __tablename__ = "users"

    customer_name = Column(String(100), unique=True, nullable=False)
    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Integer, nullable=True)
    review = Column(String(500), nullable=True)



    # Relationships
    orders = relationship("Order", back_populates="user")
    payment = relationship("Payment", back_populates="user")