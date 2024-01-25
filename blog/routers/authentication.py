from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas
from ..database import Sessionlocal
from sqlalchemy.orm import Session
from ..import models
from passlib.context import CryptContext
from datetime import timedelta
from ..token import create_access_token
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

@router.post('/login')
def login(request:schemas.Login,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid credential')
    if not pwd_cxt.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid credential')
    
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {'user':user,'token':access_token}