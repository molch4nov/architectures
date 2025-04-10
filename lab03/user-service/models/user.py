from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy import Column, String, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserType(str, Enum):
    customer = "customer"
    specialist = "specialist"
    admin = "admin"

# SQLAlchemy ORM Model
class UserORM(Base):
    __tablename__ = "users"
    
    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    type = Column(SQLAEnum(UserType), nullable=False, default=UserType.customer)
    password = Column(String, nullable=False)

# Pydantic Models
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