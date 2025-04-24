from pydantic import BaseModel, Field
from typing import Optional, List, Any
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class ServiceBase(BaseModel):
    name: str
    description: str
    category: str
    price: Decimal
    duration: int

class ServiceCreate(ServiceBase):
    specialist_id: UUID

class ServiceDB(ServiceBase):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    specialist_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
            Decimal: lambda d: str(d)
        }

class ServiceResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: str
    duration: int
    specialist_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        from_attributes = True

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None 
    category: Optional[str] = None
    price: Optional[Decimal] = None
    duration: Optional[int] = None 