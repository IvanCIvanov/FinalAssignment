from . import orders, order_details, recipes, sandwiches, resources, menu_items, users, payments

from ..dependencies.database import Base, engine


def index():
    Base.metadata.create_all(bind=engine)



