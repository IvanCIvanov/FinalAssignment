from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    order_details_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    sandwich_id = Column(Integer, ForeignKey("menu_items.id"))
    amount = Column(Integer, index=True, nullable=False)

    menu_item = relationship("MenuItem", back_populates="order_details")
    order = relationship("Order", back_populates="order_details")
