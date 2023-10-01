import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from middleware import access_control
from api import auth # api가 동작할 수 있도록 main에 추가
from api import test
from api import robot
from api import run
from api import dib
from api import log
from api.socketserver import sio_app


app = FastAPI()


# 소켓 연결
# app.mount("/", app=sio_app)


# api가 동작할 수 있도록 main에 추가
app.include_router(auth.router)
app.include_router(test.router)
app.include_router(robot.router)
app.include_router(run.router)
app.include_router(dib.router)
app.include_router(log.router)

origins = [
    "http://localhost:8080",
    "http://j9b201.p.ssafy.io"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # cross-origin request에서 cookie를 포함할 것인지 (default=False)
    allow_methods=["*"],     # cross-origin request에서 허용할 method들을 나타냄. (default=['GET']
    allow_headers=["*"],     # cross-origin request에서 허용할 HTTP Header 목록
)

ALLOW_SITE = ['*']
EXCEPTION_PATH_LIST = ['/', 'auth']
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_SITE,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control) # 미들웨어 추가

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
