from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

from jwt.exceptions import InvalidTokenError

from .token_info import TokenInfo
from .schemas import UserCreate, UserLogin

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from api_v1.auth.utils import *


router = APIRouter(prefix="/users", tags=["Users"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")
http_bearer = HTTPBearer()

@router.post("/sign_up/")
async def create_user(user: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_user(user=user, session=session)

@router.post("/login/", response_model=TokenInfo)
async def auth_user(user: UserLogin, session: AsyncSession = Depends(db_helper.session_dependency)):
    if not (user := await crud.validate_user(username=user.username, password=user.password, email=user.email, session=session)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid data"
        )

    jwt_payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }

    token = encode_jwt(payload=jwt_payload)

    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


async def get_users_payload(
    # token: str = Depends(oauth2_scheme)
    cred: HTTPAuthorizationCredentials= Depends(http_bearer)
):

    token = cred.credentials
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="time token"
        )

    return payload


@router.get('/me/')
async def auth_user_info(
    payload = Depends(get_users_payload)
):
    return payload