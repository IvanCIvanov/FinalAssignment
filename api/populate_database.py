import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from api.dependencies.database import engine, Base, get_db
from api.models import model_loader
from fastapi import Depends

# Import all models to ensure they're registered with SQLAlchemy
from .models import orders, order_details, users, payments, menu_items, recipes, resources, sandwiches

# Create all tables
Base.metadata.create_all(bind=engine)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load sample data
with open(os.path.join(script_dir, 'sample_data.json'), 'r') as f:
    sample_data = json.load(f)

def populate_database(db: Session = Depends(get_db)):
    # Populate resources
    for resource in sample_data['resources']:
        print(resource)
        db.add(resources.Resource(**resource))

    db.commit()

    # Populate sandwiches
    for sandwich in sample_data['sandwiches']:
        db.add(sandwiches.Sandwich(**sandwich))

    db.commit()

    # Populate users
    for user in sample_data['users']:
        db.add(users.User(**user))

    db.commit()

    # Populate recipes
    for recipe in sample_data['recipes']:
        db.add(recipes.Recipe(**recipe))

    db.commit()

    # Populate menu items
    for item in sample_data['menu_items']:
        if item['expiration_date']:
            item['expiration_date'] = datetime.fromisoformat(item['expiration_date'])
        db.add(menu_items.MenuItem(**item))

    db.commit()

    # Populate orders
    for order in sample_data['orders']:
        db.add(orders.Order(**order))

    db.commit()

    # Populate order details
    for detail in sample_data['order_details']:

        db.add(order_details.OrderDetail(**detail))

    db.commit()

    # Populate payments
    for payment in sample_data['payments']:
        db.add(payments.Payment(**payment))

    db.commit()

    print("Database populated successfully!")

if __name__ == "__main__":
    # This allows you to run the script directly
    db = next(get_db())
    populate_database(db)