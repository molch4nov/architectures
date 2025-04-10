from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests
import os
from typing import Optional

USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL", "http://user-service:8000")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        response = requests.post(
            f"{USER_SERVICE_URL}/validate-token", 
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            raise credentials_exception
            
        user_data = response.json()
        return {
            "user_id": user_data["user_id"],
            "user_type": user_data["user_type"]
        }
    except requests.RequestException as e:
        print(f"Error connecting to user service: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"User service is unavailable: {str(e)}"
        )
    except Exception as e:
        print(f"Other error during token validation: {str(e)}")
        raise credentials_exception 