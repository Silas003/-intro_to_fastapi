from fastapi import APIRouter
from fastapi import Depends,status,HTTPException 
from .. import schemas
from .. import models
from ..database import Sessionlocal
from sqlalchemy.orm import Session


router=APIRouter(
    prefix='/blog',
    tags=['blog']
)


def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.get('',status_code=status.HTTP_200_OK)
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs


@router.post('',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id,db:Session=Depends(get_db)):
    if not db.query(models.Blog).filter(models.Blog.id==id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'{id} does not exist')
    else:
        db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
        db.commit()
        return 'done'



@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog:
        db.query(models.Blog).filter(models.Blog.id==id).update({'title':request.title,'body':request.body})
        db.commit()
        return {'detail':f'blog with id: {id} updated'}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'blog with id:{id} does not exist')
    
    
@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def retrieve(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} does not exist')
    return blog
