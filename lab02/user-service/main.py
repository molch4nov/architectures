from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from routes import user_router
from auth import get_current_user
import json
import os

app = FastAPI(title="User Service API", 
              description="Микросервис для управления пользователями и аутентификации")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],    
)

app.include_router(user_router.router)

@app.get("/")
async def root():
    return {"message": "User Service API"}

def generate_openapi_json():
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes
    )
    
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f)

generate_openapi_json()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 