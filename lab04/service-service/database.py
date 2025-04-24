import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла (если есть)
load_dotenv()

# Получение переменных окружения
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://mongo:mongo@mongodb:27017/")
MONGO_DB = os.getenv("MONGO_DB", "service_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "services")

# Создаем клиент для MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)

# Получаем базу данных
db: Database = client[MONGO_DB]

# Получаем коллекцию
services_collection: Collection = db[MONGO_COLLECTION]

# Создаем индексы для ускорения запросов
services_collection.create_index("category")
services_collection.create_index("specialist_id")
services_collection.create_index([("name", "text"), ("description", "text")])

logging.info(f"Connected to MongoDB: {MONGO_DB}.{MONGO_COLLECTION}")

def fill_test_data():
    """Заполняет коллекцию тестовыми данными, если она пуста"""
    if services_collection.count_documents({}) == 0:
        from datetime import datetime
        from uuid import uuid4
        from decimal import Decimal
        
        test_services = [
            {
                "name": "Уборка квартиры",
                "description": "Полная уборка квартиры, включая мытье окон",
                "category": "Уборка",
                "price": "2000.00",
                "duration": 120,
                "specialist_id": str(uuid4()),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Выгул собаки",
                "description": "Выгул собаки в парке, включая игры и тренировку",
                "category": "Уход за животными",
                "price": "500.00",
                "duration": 60,
                "specialist_id": str(uuid4()),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Доставка продуктов",
                "description": "Доставка продуктов из магазина",
                "category": "Доставка",
                "price": "300.00",
                "duration": 40,
                "specialist_id": str(uuid4()),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        services_collection.insert_many(test_services)
        logging.info(f"Test data inserted: {len(test_services)} services") 