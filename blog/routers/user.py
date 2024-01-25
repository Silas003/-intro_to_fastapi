from fastapi import APIRouter
from fastapi import Depends,HTTPException ,status
from .. import schemas
from .. import models

from ..database import Sessionlocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router=APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()

pwd_cxt=CryptContext(schemes=['bcrypt'],deprecated='auto')

@router.post('',status_code=status.HTTP_201_CREATED)
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashedPassword=pwd_cxt.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=schemas.UserResponse,status_code=status.HTTP_200_OK)
def retrieve_user(id,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'user not found')