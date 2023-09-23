import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from middleware import access_control
from api import auth # api가 동작할 수 있도록 main에 추가
from api import test
from api import robot

app = FastAPI()

# api가 동작할 수 있도록 main에 추가
app.include_router(auth.router)
app.include_router(test.router)
app.include_router(robot.router)

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

    # main.py를 실행할 때만 FastAPI 서버를 시작
    uvicorn.run('main:app', reload = True)
