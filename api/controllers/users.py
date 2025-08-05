from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from ..dependencies.database import get_db
from ..models import users as user_model
from ..schemas import users as user_schema


def create(db: Session, request):
    new_item = user_model.User(
        customer_name=request.customer_name,
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

def read_all(db: Session = Depends(get_db)):
    return db.query(user_model.User).all()


def read_one(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.customer_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def update(user_id: int, updated_user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.customer_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = updated_user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.customer_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return


