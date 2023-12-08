import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from UserModel import User
from jwt import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login",  # 指定OAuth2PasswordRequestForm的路径，使用相对url
    scheme_name="JWT-ano"
)


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[float] = None

    # def is_expired(self) -> bool:
    #     return datetime.utcnow() > self.exp


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        payload_dict = eval(token_data.sub)
        payload_class = User(**payload_dict)
        exp_time = datetime.fromtimestamp(token_data.exp)
        time_now = datetime.now()
        if exp_time < time_now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:  # (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload_dict is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    if payload_class.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user does not have permission !",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload_dict
