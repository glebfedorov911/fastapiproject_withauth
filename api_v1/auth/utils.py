import jwt
import bcrypt

from core.config import settings

from datetime import timedelta, datetime


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth.private_key.read_text(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_time: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_time:
        expire = now + expire_time
    else:
        expire = now + timedelta(minutes=expire_minutes)
    
    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm
    )

    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth.public_key.read_text(),
    algorithm: str = settings.auth.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm]
    )

    return decoded

def hash_password(
    password: str
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode("utf-8")

    return bcrypt.hashpw(password=pwd_bytes, salt=salt)

def validate_password(
    password: str,
    hash_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password,
        hashed_password=hash_password
    )