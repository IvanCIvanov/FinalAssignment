from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("menu_items.sandwich_id"))
    ingredient_id = Column(Integer, ForeignKey("resources.ingredient_id"))

    menu_item = relationship("MenuItem", back_populates="recipe")
    ingredient = relationship("Resource", back_populates="recipes")