from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import payments as model
from ..models.menu_items import MenuItem
from ..models.orders import Order
from ..models.order_details import OrderDetail
from ..models.recipes import Recipe
from ..models.resources import Resource
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from sqlalchemy import func
from decimal import Decimal


def create(db: Session, request):
    new_item = model.Payment(
        id=request.id,
        payment_type = request.payment_type,
        order_id = request.order_id,
        customer_id=request.customer_id,
        payment_date = request.payment_date,
        amount_paid=request.amount_paid
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        payments = db.query(model.Payment).all()
        # Convert SQLAlchemy objects to dictionaries for JSON serialization
        result = []
        for payment in payments:
            # Convert payment_date to date-only if it's a datetime
            payment_date = payment.payment_date
            if isinstance(payment_date, datetime):
                payment_date = payment_date.date()
            elif payment_date is not None:
                payment_date = payment_date.isoformat()
            
            payment_dict = {
                "id": payment.id,
                "customer_id": payment.customer_id,
                "order_id": payment.order_id,
                "payment_type": payment.payment_type,
                "payment_date": payment_date,
                "amount_paid": str(payment.amount_paid) if hasattr(payment, 'amount_paid') else '0.00'
            }
            result.append(payment_dict)
        return result
    except Exception as e:
        error_detail = str(e)
        if hasattr(e, '__dict__') and 'orig' in e.__dict__:
            error_detail = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving payments: {error_detail}"
        )


def read_one(db: Session, item_id: int):
    try:
        payment = db.query(model.Payment).filter(model.Payment.id == item_id).first()
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found!")
        
        # Convert payment_date to date-only if it's a datetime
        payment_date = payment.payment_date
        if isinstance(payment_date, datetime):
            payment_date = payment_date.date()
        elif payment_date is not None:
            payment_date = payment_date.isoformat()
        
        return {
            "id": payment.id,
            "customer_id": payment.customer_id,
            "order_id": payment.order_id,
            "payment_type": payment.payment_type,
            "payment_date": payment_date,
            "amount_paid": str(payment.amount_paid) if hasattr(payment, 'amount_paid') else '0.00'
        }
        
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete(db: Session, item_id):
    try:
        item = db.query(model.Payment).filter(model.Payment.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_daily_profit(db: Session, target_date: date):
    # Get all payments for the target date
    payments = db.query(model.Payment)\
        .filter(func.date(model.Payment.payment_date) == target_date)\
        .all()
    
    total_profit = Decimal('0.00')
    
    for payment in payments:
        # Get the order for this payment
        order = db.query(Order).filter(Order.id == payment.order_id).first()
        if not order:
            continue
            
        # Check if there's a promotion for this sandwich
        menu_item = db.query(MenuItem).filter(MenuItem.sandwich_id == order.sandwich_id).first()
        
        # Get the payment amount
        amount = payment.amount_paid if hasattr(payment, 'amount_paid') else Decimal('0.00')
        
        # Apply 10% discount if promotion exists
        if menu_item and hasattr(menu_item, 'promotion_code') and menu_item.promotion_code:
            amount = amount * Decimal('0.9')  # 10% off
            
        total_profit += amount
    
    return float(total_profit)  # Return as float for JSON serialization
