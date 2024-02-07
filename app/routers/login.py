"""Login authorisation"""
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database
from app import models
from app import token
from app import  utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def create_login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                 db: Session = Depends(database.get_db)):
    """Login to generate token"""
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")

    if not utils.verify_login(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")
    access_token = token.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
