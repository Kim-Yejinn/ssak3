from fastapi import FastAPI
import uvicorn
from sockets import sio_app

#
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.middleware.cors import CORSMiddleware
#
# from middleware import access_control
# from api import auth # auth api가 동작할 수 있도록 main에 추가

app = FastAPI()

# app.include_router(auth.router) # auth api가 동작할 수 있도록 main에 추가

# ALLOW_SITE = ['*']
# EXCEPTION_PATH_LIST = ['/', 'auth']
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOW_SITE,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
# app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control) # 미들웨어 추가


app.mount("/", app=sio_app)


@app.get("/")
async def root():
    return {"test": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    # main.py를 실행할 때만 FastAPI 서버를 시작
    uvicorn.run('main:app', reload=True)
