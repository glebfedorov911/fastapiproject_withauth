from fastapi import HTTPException, status, Form

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select

from core.models import User
from .schemas import UserCreate, UserLogin
from api_v1.auth.utils import *

from sqlalchemy.exc import IntegrityError



async def create_user(user: UserCreate, session: AsyncSession):
    if not len(user.password) > 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid password"
        )

    try:
        user.password = hash_password(user.password.decode("utf-8"))

        new_user = User(**user.model_dump())
        session.add(new_user)
        await session.commit()

        return new_user

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email or username already exist"
        )

async def validate_user(
    username: str,
    password: str,
    email: str,
    session: AsyncSession
):  

    stmt = select(User).where(User.email == email).where(User.username==username)
    result: Result = await session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unknown username or email"
        )

    user = await session.get(User, int(user.id))
    
    if not validate_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid password"
        )
    
    return user

