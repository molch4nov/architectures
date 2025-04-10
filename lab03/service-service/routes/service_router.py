from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID, uuid4

from models.service import ServiceCreate, ServiceResponse
from database import services
from auth import get_current_user

router = APIRouter(tags=["services"])

@router.post("/services/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(service: ServiceCreate, current_user: dict = Depends(get_current_user)):
    if current_user["user_type"] != "specialist" and current_user["user_type"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only specialists can create services"
        )
    
    if current_user["user_type"] != "admin" and str(current_user["user_id"]) != str(service.specialist_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can create services only for yourself"
        )
    
    service_id = uuid4()
    new_service = {
        "id": service_id,
        "name": service.name,
        "description": service.description,
        "category": service.category,
        "price": service.price,
        "duration": service.duration,
        "specialist_id": service.specialist_id
    }
    services[service_id] = new_service
    
    return {"id": service_id, **new_service}

@router.get("/services/", response_model=List[ServiceResponse])
async def get_services(category: Optional[str] = None):
    if category:
        return [
            {"id": service_id, **service}
            for service_id, service in services.items()
            if service["category"] == category
        ]
    return [{"id": service_id, **service} for service_id, service in services.items()]

@router.get("/services/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: UUID):
    if service_id not in services:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    service = services[service_id]
    return {"id": service_id, **service}

@router.get("/services/specialist/{specialist_id}", response_model=List[ServiceResponse])
async def get_specialist_services(specialist_id: UUID):
    specialist_services = [
        {"id": service_id, **service}
        for service_id, service in services.items()
        if service["specialist_id"] == specialist_id
    ]
    
    if not specialist_services:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No services found for this specialist"
        )
    
    return specialist_services 