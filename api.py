from starlette.responses import JSONResponse

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jwt import verify_password, create_access_token
from UserModel import User
from deps import get_current_user

apiRouter = APIRouter(
    prefix="/api/v1",
    tags=['jwt_test']
)
fake_user_db = {
    'username': 'ano',
    'hash_password': '$2b$12$OGuEGI58uOBemfet6Z22Ku26hRVvY1F5mm5YJ2krRG3cC26TSNdoO',  # 123
    'sex': '男',
    'email': '2478664861@qq.com',
    'active': True,
    'role': "admin0",
}


@apiRouter.post("/login", summary="user login")
async def user_login(from_data: OAuth2PasswordRequestForm = Depends()):
    user_db = User(**fake_user_db)
    if user_db.active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='input user is not active!'
        )
    if not verify_password(from_data.password, user_db.hash_password) or from_data.username != user_db.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='illegal username or password'
        )
    try:
        resp = {
            # 'id': str(uuid4()),
            "access_token": create_access_token(
                user_db.__dict__
            ),
            "token_type": "bearer",
        }
        resp.update(fake_user_db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='build resp fail = ' + str(type(e))
        )
        # return中必须包含"access_token": create_access_token(userdb)
    return JSONResponse(status_code=200, content=resp)


@apiRouter.get("/jwt_deps", summary="need jwt")
async def jwt_deps(now_user=Depends(get_current_user)):
    return JSONResponse(status_code=200, content=now_user)
