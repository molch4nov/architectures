from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from bson import ObjectId
from models.service import ServiceCreate, ServiceResponse, ServiceUpdate
from database import services_collection
from auth import get_current_user, get_admin_user

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
    
    new_service = {
        "name": service.name,
        "description": service.description,
        "category": service.category,
        "price": str(service.price),
        "duration": service.duration,
        "specialist_id": str(service.specialist_id),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = services_collection.insert_one(new_service)
    created_service = services_collection.find_one({"_id": result.inserted_id})
    
    return {
        "id": str(created_service["_id"]),
        **created_service
    }

@router.get("/services/", response_model=List[ServiceResponse])
async def get_services(
    category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    query = {}
    
    if category:
        query["category"] = category
    
    if search:
        query["$text"] = {"$search": search}
    
    services = services_collection.find(query).skip(skip).limit(limit)
    
    return [{
        "id": str(service["_id"]),
        **{k: v for k, v in service.items() if k != "_id"}
    } for service in services]

@router.get("/services/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: str):
    try:
        service = services_collection.find_one({"_id": ObjectId(service_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid service ID format"
        )
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return {
        "id": str(service["_id"]),
        **{k: v for k, v in service.items() if k != "_id"}
    }

@router.get("/services/specialist/{specialist_id}", response_model=List[ServiceResponse])
async def get_specialist_services(specialist_id: UUID):
    services = services_collection.find({"specialist_id": str(specialist_id)})
    result = [{
        "id": str(service["_id"]),
        **{k: v for k, v in service.items() if k != "_id"}
    } for service in services]
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No services found for this specialist"
        )
    
    return result

@router.put("/services/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: str, 
    service_update: ServiceUpdate, 
    current_user: dict = Depends(get_current_user)
):
    try:
        service = services_collection.find_one({"_id": ObjectId(service_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid service ID format"
        )
        
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    if current_user["user_type"] != "admin" and str(current_user["user_id"]) != service["specialist_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your own services"
        )
    
    update_data = {k: v for k, v in service_update.dict(exclude_unset=True).items() if v is not None}
    
    if "price" in update_data:
        update_data["price"] = str(update_data["price"])
    
    update_data["updated_at"] = datetime.utcnow()
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    services_collection.update_one(
        {"_id": ObjectId(service_id)},
        {"$set": update_data}
    )
    
    updated_service = services_collection.find_one({"_id": ObjectId(service_id)})
    
    return {
        "id": str(updated_service["_id"]),
        **{k: v for k, v in updated_service.items() if k != "_id"}
    }

@router.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: str, 
    current_user: dict = Depends(get_current_user)
):
    try:
        service = services_collection.find_one({"_id": ObjectId(service_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid service ID format"
        )
        
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    if current_user["user_type"] != "admin" and str(current_user["user_id"]) != service["specialist_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can delete only your own services"
        )
    
    services_collection.delete_one({"_id": ObjectId(service_id)}) 