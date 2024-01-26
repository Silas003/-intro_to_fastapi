from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from .import token
from typing import Annotated
from jose import jwt,JWTError
from .schemas import TokenData


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='could not validate credentials',
        headers={'www-Authenticate':'Bearer'}
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str=payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data=TokenData(email=email)
        print(token_data)
        return token_data
    except JWTError:
        raise credentials_exception

    
   
     