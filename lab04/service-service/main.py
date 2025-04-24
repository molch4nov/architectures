from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from routes import service_router
from database import fill_test_data

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Service Service API",
    description="API для работы с услугами",
    version="1.0.0",
)

# Добавление CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавление маршрутов
app.include_router(service_router, prefix="/api")

@app.on_event("startup")
async def startup_db_client():
    # Заполнение тестовыми данными при запуске
    fill_test_data()
    logging.info("Service Service API started")

@app.on_event("shutdown")
async def shutdown_db_client():
    from database import client
    client.close()
    logging.info("MongoDB connection closed")

@app.get("/health")
async def health_check():
    return {"status": "ok"} 