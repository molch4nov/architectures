from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from uuid import UUID, uuid4
from datetime import timedelta

from models.user import UserCreate, UserResponse, Token
from database import users
from auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user

router = APIRouter(tags=["users"])

# Маршрут для получения токена (авторизация)
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "type": user["type"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Маршруты для пользователей
@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Проверяем, нет ли пользователя с таким email
    for existing_user in users.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Создаем нового пользователя
    user_id = uuid4()
    new_user = {
        "id": user_id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "type": user.type,
        "password": user.password  # В реальном приложении хешируем пароль
    }
    users[user_id] = new_user
    
    # Возвращаем данные пользователя без пароля
    return {"id": user_id, **user.dict(exclude={"password"})}

@router.get("/users/", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_user)):
    # Проверяем права доступа: только админ может видеть всех пользователей
    if current_user["type"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return [{"id": user_id, **{k: v for k, v in user.items() if k != "password"}} 
            for user_id, user in users.items()]

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, current_user: dict = Depends(get_current_user)):
    # Пользователь может получить только свои данные или админ может видеть любые
    if str(current_user["id"]) != str(user_id) and current_user["type"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = users[user_id]
    return {"id": user_id, **{k: v for k, v in user.items() if k != "password"}}

@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"id": current_user["id"], **{k: v for k, v in current_user.items() if k != "password"}}

# Эндпоинт для проверки валидности токена - служебный, для использования другими сервисами
@router.post("/validate-token")
async def validate_token(current_user: dict = Depends(get_current_user)):
    return {"valid": True, "user_id": current_user["id"], "user_type": current_user["type"]} 