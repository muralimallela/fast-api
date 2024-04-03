from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class UserOut(BaseModel):
    id : int 
    email : EmailStr
    created_at : datetime
    
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at : datetime
    owner : UserOut

class PostOut(BaseModel):
    Posts: Post
    votes: int
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int 
    email : EmailStr
    created_at : datetime
    
# class User_credentials(BaseModel):
#     email : EmailStr
#     password : str
    
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str]= None
    
class Vote(BaseModel):
    post_id : int
    dire : int = conint(le = 1 , ge =0)