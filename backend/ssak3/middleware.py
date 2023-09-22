import os
import re

import jwt
from jwt.exceptions import ExpiredSignature, DecodeError
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.requests import Request
# from starlette.datastructures import URL, Headers
from starlette.responses import JSONResponse

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
EXCEPT_PATH_LIST = ['/', '/auth', '/docs', '/redoc', '/openapi.json']
EXCEPT_PATH_REGEX = "^(/docs|/redoc)"

async def access_control(request: Request, call_next):
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    headers = request.headers.get("AUTHORIZATION") # 요청 헤더에서 토큰 빼오기
    origin_url =request.url.path
    # print("origin_url"+origin_url)
    if origin_url in EXCEPT_PATH_LIST or origin_url.startswith("/auth"): # 검사 안해도 되는 요청이면 토큰검사 안하고 넘김
        response = await call_next(request)
        return response

    # 나머지 요청을 토큰 검사 함
    token = await token_decode(headers)
    response = call_next(request)
    return response




# async def url_pattern_check(path, pattern): # 경로가 pattern에 있는지 확인
#     result = re.match(pattern, path)
#     if result:
#         return True
#     return False

async def token_decode(access_token): # 토큰 암호화 풀기
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="토큰이 없다..")
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
    except ExpiredSignature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="(액세스) 토큰 만료")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="비정상적인 접근입니다.")
    return payload

import os

import jwt
from jwt.exceptions import ExpiredSignature, DecodeError
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.requests import Request

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
EXCEPT_PATH_LIST = ['/', '/auth', '/docs', '/redoc', '/openapi.json']

async def access_control(request: Request, call_next):
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    headers = request.headers.get("Authorization") # 요청 헤더에서 토큰 빼오기
    origin_url =request.url.path
    # print("origin_url"+origin_url)
    if origin_url in EXCEPT_PATH_LIST or origin_url.startswith("/"): # 검사 안해도 되는 요청이면 토큰검사 안하고 넘김. "/"이면 개발용으로 열어놓은 상태. "/auth"으로 바꿔주기
        response = await call_next(request)
        return response

    # 나머지 요청을 토큰 검사 함
    payload = await token_decode(headers)
    request.state.user = payload
    if payload.get("type") == "rtk" and origin_url=="/auth/retoken": #토큰 재발급
        response = await call_next(request)
        return response
    response = await call_next(request)
    return response

async def token_decode(access_token): # 토큰 암호화 풀기
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="토큰이 없다..")
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
    except ExpiredSignature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="(액세스) 토큰 만료")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="비정상적인 접근입니다.")
    return payload
