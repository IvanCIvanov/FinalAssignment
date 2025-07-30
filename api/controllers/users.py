from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import users as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.User(
        customer_id=request.customer_id,
        rating=request.rating,
        review=request.review
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


