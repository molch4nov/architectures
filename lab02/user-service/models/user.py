from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

class UserType(str, Enum):
    customer = "customer"
    specialist = "specialist"
    admin = "admin"

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    type: UserType = UserType.customer

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: UUID
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
    user_id: UUID = None
    user_type: UserType = None 