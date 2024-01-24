from fastapi import FastAPI,Depends,status,Response,HTTPException 
from . import schemas
from . import models
from fastapi.openapi.utils import get_openapi
from .database import engine,Sessionlocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
app=FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

models.Base.metadata.create_all(engine)

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blog'])
def create(request:schemas.Blog, db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blog'])
def delete(id,db:Session=Depends(get_db)):
    if not db.query(models.Blog).filter(models.Blog.id==id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'{id} does not exist')
    else:
        db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
        db.commit()
        return 'done'



@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blog'])
def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog:
        db.query(models.Blog).filter(models.Blog.id==id).update({'title':request.title,'body':request.body})
        db.commit()
        return {'detail':f'blog with id: {id} updated'}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'blog with id:{id} does not exist')

@app.get('/blog',status_code=status.HTTP_200_OK,tags=['blog'])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs



@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog,tags=['blog'])
def retrieve(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} does not exist')
    return blog

pwd_cxt=CryptContext(schemes=['bcrypt'],deprecated='auto')

@app.post('/user',status_code=status.HTTP_201_CREATED,tags=['user'])
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashedPassword=pwd_cxt.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}',response_model=schemas.UserResponse,status_code=status.HTTP_200_OK,tags=['user'])
def retrieve_user(id,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'user not found')