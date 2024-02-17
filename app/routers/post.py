"""posts path operation"""
from typing import List, Optional
from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(
    prefix="/saposts", # So that we don't need to define in decorator
    tags=['Posts'] # To group api docs
)

@router.get("/", response_model=List[schemas.Response])
def test_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): # Will create database defined in models.py
    """Test Sqlalchemy model"""
    print(current_user.email)
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # Get all posts
    return posts

@router.get("/{my_id}", response_model=schemas.Response)
                             # matches to a url where given value
                             # in the root is mapped to id variable
# def get_post(id: int, response: Response):
def get_sapost(my_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Get a given post by id"""
    print(current_user.email)
    post = db.query(models.Post).filter(models.Post.id == my_id).first()
    # post = find_post(int(my_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {my_id} was not found")
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"message": f"Post with id: {id} was not found"}
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def create_sapost(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
                                                                # Create post using sqlalchemy
    """Create a new post"""
#    new_post = models.Post(title=post.title, content=post.content, published=post.published)
#    There is an efficient way of doing
    print(current_user.email)
    new_post = models.Post(created_by = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{my_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sapost(my_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Delete a post"""
    print(current_user.email)
    post_qry = db.query(models.Post).filter(models.Post.id == my_id)
    existing_post = post_qry.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {my_id} was not found")
    
    if existing_post.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    post_qry.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{my_id}")
def update_sapost(my_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Update a post"""
    print(current_user.email)
    post_qry = db.query(models.Post).filter(models.Post.id == my_id)
    existing_post = post_qry.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {my_id} was not found")
    
    if existing_post.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    
    post_qry.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return {"data": post_qry.first()}
