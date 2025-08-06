import click
from sqlalchemy import create_engine, func, and_, or_
from sqlalchemy.orm import sessionmaker, joinedload, contains_eager
from datetime import datetime, timedelta
import sys
import os
from urllib.parse import quote_plus

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import database configuration
from api.dependencies.config import conf

# Import your models
from api.models.orders import Order
from api.models.users import User
from api.models.sandwiches import Sandwich
from api.models.recipes import Recipe
from api.models.resources import Resource
from api.models.order_details import OrderDetail
from api.models.payments import Payment
from api.models.menu_items import MenuItem

# Database connection setup using the project's configuration
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.db_user}:{quote_plus(conf.db_password)}@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_user_orders():
    """Test joining users with their orders"""
    db = next(get_db())
    try:
        # Explicitly join with User and select needed fields
        results = db.query(
            Order,
            User.customer_name
        ).join(
            User, Order.user_id == User.customer_id
        ).all()
        
        print("\n=== User Orders ===")
        for order, customer_name in results:
            print(f"Order ID: {order.id}, "
                  f"Customer: {customer_name}, "
                  f"Date: {order.order_date}, "
                  f"Sandwich ID: {order.sandwich_id}, "
                  f"Amount: {order.amount}")
            
        return results
    except Exception as e:
        print(f"Error in test_user_orders: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

def test_sandwich_ingredients():
    """Test joining sandwiches with their ingredients through recipes"""
    db = next(get_db())
    try:
        # Query sandwiches with their ingredients and amounts
        results = db.query(
            Sandwich,
            Resource.ingredient_name,
            Resource.amount
        ).join(
            Recipe, Sandwich.id == Recipe.sandwich_id
        ).join(
            Resource, Recipe.ingredient_id == Resource.ingredient_id
        ).all()
        
        print("\n=== Sandwich Ingredients ===")
        current_sandwich = None
        
        # Group results by sandwich
        from collections import defaultdict
        sandwich_ingredients = defaultdict(list)
        
        for sandwich, ingredient_name, amount in results:
            sandwich_ingredients[sandwich.sandwich_name].append((ingredient_name, amount))
        
        # Print the results
        for sandwich_name, ingredients in sandwich_ingredients.items():
            print(f"\n{sandwich_name}:")
            for ingredient_name, amount in ingredients:
                print(f"  - {ingredient_name}: {amount}")
            
        return results
    except Exception as e:
        print(f"Error in test_sandwich_ingredients: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

def test_orders_with_payments():
    """Test joining orders with payment information"""
    db = next(get_db())
    try:
        # Query orders with their payment information
        results = db.query(
            Order,
            Payment.payment_type
        ).outerjoin(
            Payment, Order.id == Payment.order_id
        ).join(
            User, Order.user_id == User.customer_id
        ).all()
        
        print("\n=== Orders with Payments ===")
        for order, payment_type in results:
            print(f"Order ID: {order.id}, "
                  f"Customer: {order.user.customer_name if hasattr(order, 'user') and order.user else 'Unknown'}, "
                  f"Date: {order.order_date}, "
                  f"Payment Type: {payment_type if payment_type else 'No payment'}")
            
        return results
    except Exception as e:
        print(f"Error in test_orders_with_payments: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

def filter_orders_by_date(start_date, end_date=None):
    """Helper function to filter orders by date range"""
    db = next(get_db())
    try:
        # Convert string dates to datetime objects
        start = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            condition = and_(Order.order_date >= start, Order.order_date <= end)
        else:
            condition = Order.order_date >= start
            
        # Explicitly join with related tables and select needed fields
        results = db.query(
            Order,
            User.customer_name,
            Sandwich.sandwich_name
        ).join(
            User, Order.user_id == User.customer_id
        ).join(
            Sandwich, Order.sandwich_id == Sandwich.id
        ).filter(condition).all()
        
        print(f"\n=== Orders from {start_date} {f'to {end_date}' if end_date else 'onwards'} ===")
        for order, customer_name, sandwich_name in results:
            print(f"Date: {order.order_date}, "
                  f"Customer: {customer_name}, "
                  f"Ordered: {order.amount}x {sandwich_name or 'Unknown Sandwich'}")
            
        return results
    except Exception as e:
        print(f"Error in test_filter_orders_by_date: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

def test_filter_orders():
    """Test filtering orders by date range"""
    # Test with a date range that likely has data
    # You may need to adjust these dates based on your test data
    start_date = (datetime.now().date() - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = datetime.now().date().strftime('%Y-%m-%d')
    
    # Test with date range
    results = filter_orders_by_date(start_date, end_date)
    assert results is not None
    
    # Test with start date only
    results_single = filter_orders_by_date(start_date)
    assert results_single is not None

# CLI interface
@click.group()
def cli():
    """Database query testing tool"""
    pass

@cli.command()
def user_orders():
    """Show users and their orders"""
    test_user_orders()

@cli.command()
def sandwich_ingredients():
    """Show sandwiches and their ingredients"""
    test_sandwich_ingredients()

@cli.command()
def orders_with_payments():
    """Show orders with payment information"""
    test_orders_with_payments()

@cli.command()
@click.argument('start_date')
@click.argument('end_date', required=False)
def filter_orders(start_date, end_date=None):
    """Filter orders by date range (format: YYYY-MM-DD)"""
    filter_orders_by_date(start_date, end_date)

if __name__ == '__main__':
    cli()
