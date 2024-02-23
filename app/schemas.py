"""Schema for api request and response"""
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    """Token class"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token Data"""
    id: Optional[int] = None

class UserCreate(BaseModel):
    """Base class for user table uqery"""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """Base class for user response"""
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        """Helps to convert sqlachemy model of response"""
        from_attributes = True

class UserLogin(BaseModel):
    """Base class for login"""
    email: EmailStr
    password: str

class PostBase(BaseModel):
    """Base class that will represent schema for a post"""
    title: str
    content: str
    published: bool = True
#    rating: Optional[int] = None

class PostCreate(PostBase):
    """Schema copied from Base"""

class Response(PostBase):
    """Schema for Response message"""
    id: int
    created_at: datetime
    created_by: int
    creator: UserOut
    votes: int

    class Config:
        """Helps to convert sqlachemy model of response"""
        from_attributes = True

#class PostOut(PostBase):
#
#    class Config:
#        """Helps to convert sqlachemy model of response"""
#        from_attributes = True

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1, ge=0)]
