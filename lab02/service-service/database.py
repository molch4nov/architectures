from uuid import UUID, uuid4
from decimal import Decimal
import os

# Получаем ID тестового специалиста
# В реальном приложении IDs получались бы из реального сервиса пользователей
# или из базы данных
SPECIALIST_ID = uuid4()

# Хранилище данных в памяти
services = {}

# Добавляем тестовые услуги
service_id = uuid4()
services[service_id] = {
    "id": service_id,
    "name": "Уборка квартиры",
    "description": "Полная уборка квартиры",
    "category": "Уборка",
    "price": Decimal("2000.00"),
    "duration": 120,  # 2 часа
    "specialist_id": SPECIALIST_ID
}

service_id2 = uuid4()
services[service_id2] = {
    "id": service_id2,
    "name": "Выгул собаки",
    "description": "Выгул собаки в парке",
    "category": "Уход за животными",
    "price": Decimal("500.00"),
    "duration": 60,  # 1 час
    "specialist_id": SPECIALIST_ID
} 