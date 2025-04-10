from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from decimal import Decimal

class ServiceBase(BaseModel):
    name: str
    description: str
    category: str
    price: Decimal
    duration: int

class ServiceCreate(ServiceBase):
    specialist_id: UUID

class ServiceResponse(ServiceBase):
    id: UUID
    specialist_id: UUID
    
    class Config:
        from_attributes = True 