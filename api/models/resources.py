from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    ingredient_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ingredient_name = Column(String(100), unique=True, nullable=False)
    amount = Column(Integer, nullable=False)

    recipes = relationship("Recipe", back_populates="ingredient")
