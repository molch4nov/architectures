#!/usr/bin/env python3
"""
Скрипт для наполнения базы данных MongoDB тестовыми данными.
Запускается при первом запуске сервиса.
"""

import logging
from database import services_collection, fill_test_data
from pymongo.errors import PyMongoError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

def main():
    try:
        # Очищаем коллекцию перед заполнением
        services_collection.delete_many({})
        logging.info("Services collection cleared")
        
        # Заполняем тестовыми данными
        fill_test_data()
        
        # Проверяем количество документов
        count = services_collection.count_documents({})
        logging.info(f"Services collection contains {count} documents")
        
        # Проверяем наличие индексов
        indexes = list(services_collection.list_indexes())
        logging.info(f"Services collection has {len(indexes)} indexes:")
        for idx in indexes:
            logging.info(f" - {idx['name']}: {idx['key']}")
            
    except PyMongoError as e:
        logging.error(f"MongoDB error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main() 