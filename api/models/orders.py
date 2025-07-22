from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    order_details_id = Column(Integer, ForeignKey("order_details.order_details_id"))

    order_details = relationship("OrderDetail", back_populates="order")
    user = relationship("User", back_populates="order")
    payment = relationship("Payment", back_populates="order")