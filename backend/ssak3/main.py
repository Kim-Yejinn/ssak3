from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from middleware import access_control
from api import auth # auth api가 동작할 수 있도록 main에 추가

app = FastAPI()

app.include_router(auth.router) # auth api가 동작할 수 있도록 main에 추가

# ALLOW_SITE = ['*']
# EXCEPTION_PATH_LIST = ['/', 'auth']
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOW_SITE,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control) # 미들웨어 추가
