from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    sandwich_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    recipe = relationship("Recipe", back_populates="menu_items", foreign_keys="MenuItem.recipe_id")
    order_details = relationship("OrderDetail", back_populates="menu_item")

    promotion_code = Column(String(50), nullable=True)
    expiration_date = Column(DATETIME, nullable=True)