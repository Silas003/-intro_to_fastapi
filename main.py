from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
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


app=FastAPI()

@app.get('/blog')
def index(limit:int,published:bool,sort:Optional[str] = None):
    if published:
        return {'data':f' {limit} blog list(S)'}
    return {'data':'published wasnt true'}

@app.get('/blog/unpublished')
def unpublshed():
    return {'data':'all unpublished blogs'}

@app.get('/about')
def about():
    return {'data':{'about page'}}


@app.get('/blog/{id:int}')
def show(id):
    return {'data':id}


@app.get('/blog{id}/comment')
def comment(id):
    return {'data':'particular comment'}

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]

@app.post('/blog')
def create_blog(request:Blog):
    return {'data':'Blog is created'}


# if __name__=='__main__':
#     uvicorn.run(app,host='127.0.0.1',port=100)