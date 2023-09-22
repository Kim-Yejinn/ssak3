# import uvicorn
from fastapi import FastAPI

from api import auth # auth api가 동작할 수 있도록 main에 추가

app = FastAPI()

app.include_router(auth.router) # auth api가 동작할 수 있도록 main에 추가

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# @app.get("/hello")
# def hello():
#     return {"message": "DB sqlalchemy인가 뭐시기 하는 에러가 뜨는데 쉬불탱 못해먹겠드아..."}
