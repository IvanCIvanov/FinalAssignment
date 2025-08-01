from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import sandwiches as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_sandwich = model.Sandwich(
        id=request.id,
        sandwich_name=request.sandwich_name,
        price=request.price,
    )

    try:
        db.add(new_sandwich)
        db.commit()
        db.refresh(new_sandwich)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_sandwich

def read_all(db: Session):
    try:
        result = db.query(model.Sandwich).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, sandwich_id):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, sandwich_id, request):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, sandwich_id, request):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)