from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    order_details_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Integer, index=True, nullable=False)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sandwich_id = Column(Integer, ForeignKey("menu_items.sandwich_id"), nullable=False)

    order = relationship("Order", back_populates="order_details")
    menu_item = relationship("MenuItem", back_populates="order_details")
