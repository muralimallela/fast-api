from fastapi import APIRouter, responses, status, HTTPException, Depends, Response
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func, select

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/",response_model=List[schemas.PostOut])


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    posts_query = (select(models.Posts, func.count(models.Vote.post_id).label("votes")).join(models.Vote,isouter=True).group_by(models.Posts.id))
    response = db.execute(posts_query)
    posts =   response.mappings().all()
    print(posts)

    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post of id {id} is not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Posts(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    update_post = db.query(models.Posts).filter(models.Posts.id == id)
    old_post = update_post.first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post of id {id} is not found")
    update_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    new_post = update_post.first()
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post of id {id} is not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
