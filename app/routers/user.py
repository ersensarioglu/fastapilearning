"""users path operation"""
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/users", # So that we don't need to define in decorator
    tags=['Users'] # To group api docs
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a user"""
    # Hash password in user.password
    hashed_password = utils.my_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{my_id}", response_model=schemas.UserOut)
def get_user(my_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Get a given user by id"""
    print(current_user.email)
    if current_user.id != my_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {my_id} was not found")        
    user = db.query(models.User).filter(models.User.id == my_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {my_id} was not found")
    return user
