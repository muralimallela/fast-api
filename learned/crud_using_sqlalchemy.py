
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel

from sqlalchemy.orm import Session
from . import models
from ..app.database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    
@app.get("/")
def root():
    return {"message": "Please visit 'localhost:8000/docs' for api end points"}
@app.get("/posts")
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {"data":posts}

@app.get("/posts/{id}")
def get_post(id : int,db: Session = Depends(get_db)):
    post =  db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post of id {id} is not found")
    return {"data" : post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post : Post,db:Session = Depends(get_db)):
    new_post = models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}


@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id : int,post : Post, db : Session = Depends(get_db)):
    update_post = db.query(models.Posts).filter(models.Posts.id == id)
    old_post = update_post.first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post of id {id} is not found")
    update_post.update(post.model_dump())
    db.commit()
    new_post = update_post.first()
    return {"data" : new_post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session=Depends(get_db)):
    post =  db.query(models.Posts).filter(models.Posts.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post of id {id} is not found")
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

