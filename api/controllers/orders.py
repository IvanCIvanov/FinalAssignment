from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError
from ..models.menu_items import MenuItem
from datetime import datetime
from ..models.recipes import Recipe

def create(db: Session, request):
    discount = 0
    promo_code_used = None

    if request.promo_code:
        # Step 1: Find recipes for the given sandwich
        recipe_ids = db.query(Recipe.recipe_id).filter(Recipe.sandwich_id == request.sandwich_id).subquery()

        # Step 2: Find matching promo for those recipes
        promo_item = db.query(MenuItem).filter(
            MenuItem.promotion_code == request.promo_code,
            MenuItem.recipe_id.in_(recipe_ids)
        ).first()

        if promo_item:
            if not promo_item.expiration_date or promo_item.expiration_date > datetime.utcnow():
                discount = 0.10
                promo_code_used = request.promo_code
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promo code expired.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid promo code for this sandwich.")

    new_item = model.Order(
        user_id=request.user_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {
        "order": new_item,
        "discount_applied": f"{int(discount * 100)}%" if discount else "None",
        "promo_code": promo_code_used or "None"
    }

# def create(db: Session, request):
#     new_item = model.Order(
#         customer_name=request.customer_name,
#         user_id=request.user_id,
#         sandwich_id=request.sandwich_id,
#         amount=request.amount
#     )
#
#     try:
#         db.add(new_item)
#         db.commit()
#         db.refresh(new_item)
#     except SQLAlchemyError as e:
#         error = str(e.__dict__['orig'])
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
#
#     return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
