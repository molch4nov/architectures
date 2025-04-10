from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from routes import service_router
import json
import os

app = FastAPI(title="Service Management API", 
              description="Микросервис для управления услугами")

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Подключаем роутеры
app.include_router(service_router.router)

@app.get("/")
async def root():
    return {"message": "Service Management API"}

# Создание OpenAPI спецификации и сохранение в файл
def generate_openapi_json():
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes
    )
    
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f)

# Генерируем OpenAPI спецификацию при запуске приложения
generate_openapi_json()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port) 