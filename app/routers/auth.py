from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models,utils,database,oauth2,schemas

router = APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token)
def user_login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(user_credentials.username == models.Users.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    
    return {"access_token": access_token,"token_type" : "bearer"}