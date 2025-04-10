from uuid import UUID, uuid4
from decimal import Decimal
import os

SPECIALIST_ID = uuid4()

services = {}

service_id = uuid4()
services[service_id] = {
    "id": service_id,
    "name": "Уборка квартиры",
    "description": "Полная уборка квартиры",
    "category": "Уборка",
    "price": Decimal("2000.00"),
    "duration": 120,
    "specialist_id": SPECIALIST_ID
}

service_id2 = uuid4()
services[service_id2] = {
    "id": service_id2,
    "name": "Выгул собаки",
    "description": "Выгул собаки в парке",
    "category": "Уход за животными",
    "price": Decimal("500.00"),
    "duration": 60,
    "specialist_id": SPECIALIST_ID
} 