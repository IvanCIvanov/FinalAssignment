from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column("recipe_id", Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    ingredient_id = Column("ingredient_id", Integer, ForeignKey("resources.ingredient_id"))

    menu_items = relationship("MenuItem", back_populates="recipe")
    ingredient = relationship("Resource", back_populates="recipes", foreign_keys="Recipe.ingredient_id")
    sandwich = relationship("Sandwich", back_populates="recipes")