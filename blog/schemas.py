from pydantic import BaseModel


class Blog(BaseModel):
    title:str
    body:str

class User(BaseModel):
    name:str
    email:str
    password:str
    


class UserResponse(BaseModel):
    
    name:str
    email:str
    class Config:
        orm_mode=True
        
class ShowBlog(BaseModel):
    title:str
    body:str
    author:UserResponse
    class Config:
        orm_mode=True