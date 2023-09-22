from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request

router = APIRouter()

#security 확인용 api 완성되면 파일 삭제할 것
@router.get("/test")
async def test(request: Request):
    print(request.state.user)
    # userId = request.state.user.get("sub") # 토큰에서 가져온 아이디로 사용자검증 할거임
    # print(userId)
    return "하이"