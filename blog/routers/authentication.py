from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas
from ..database import Sessionlocal
from sqlalchemy.orm import Session
from ..import models
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from .. import token
from datetime import timedelta
from typing import Annotated

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router=APIRouter(
    tags=['authentication']
)


def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()
      
pwd_cxt=CryptContext(schemes=['bcrypt'],deprecated='auto')  

# @router.post('/login')
# def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
#     user=db.query(models.User).filter(models.User.email==request.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid credential')
#     if not pwd_cxt.verify(request.password,user.password):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid credential')
    
    
#     access_token = token.create_access_token(
#         data={"sub": user.email}
#     )
#     return {'token':access_token,'token_type':'bearer'}

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(get_db)
) -> schemas.Token:
    user =db.query(models.User).filter(models.User.email==form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")