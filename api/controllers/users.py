from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends, APIRouter
from ..models import users as model
from sqlalchemy.exc import SQLAlchemyError
from ..dependencies.database import get_db
from ..models import users as user_model
from ..schemas import users as user_schema

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    new_user = user_model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/create_Database",)




@router.get("/", response_model=list[user_schema.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(user_model.User).all()

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.customer_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, updated_user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.customer_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = updated_user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.customer_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return

#def create(db: Session, request):
    #new_item = model.User(
        #customer_id=request.customer_id,
        #rating=request.rating,
        #review=request.review
    #)

    #try:
    #     db.add(new_item)
    #     db.commit()
    #     db.refresh(new_item)
    # except SQLAlchemyError as e:
    #     error = str(e.__dict__['orig'])
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    #
    # return new_item

def read_all(db: Session):
    try:
        result = db.query(model.User).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id):
    try:
        item = db.query(model.User).filter(model.User.customer_id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def delete(db: Session, item_id):
    try:
        item = db.query(model.User).filter(model.User.customer_id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def update(db: Session, item_id, request):
    try:
        item = db.query(model.User).filter(model.User.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

