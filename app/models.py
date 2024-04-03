from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String(45),nullable=False,unique=True)
    password = Column(String(250),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
    
class Posts(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String(45),nullable=False)
    content = Column(String(45),nullable=False)
    published = Column(Boolean,server_default="1",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("Users")
    
class Vote(Base):
    __tablename__= "votes"
    
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)