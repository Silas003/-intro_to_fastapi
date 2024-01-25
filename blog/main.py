from fastapi import FastAPI
from . import models
from fastapi.openapi.utils import get_openapi
from .database import engine
from .routers import blog,user,authentication
app=FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Intro to fastapi",
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
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(engine)








