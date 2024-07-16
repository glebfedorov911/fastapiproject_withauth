from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: bytes
    email: EmailStr

class UserLogin(UserCreate):    
    ...