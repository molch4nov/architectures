# Лабораторная работа 4

## Задание

1. Для одного сервиса управления данными (созданного в предыдущих лабораторных работах) создайте долговременное хранилище данных в noSQL базе данных MongoDB (4.0 или 5.0);
2. Выберете любой сервис, не связанный с клиентскими данными (клиентский сервис остается в PostgreSQL). Например, данные о поездках, данные о планах, данные о сообщениях...;
3. Должен быть создан скрипт по наполнению СУБД тестовыми значениями. Он должен запускаться при первом запуске вашего сервиса;
4. Для сущности, должны быть созданы запросы к БД (CRUD) согласно ранее разработанной архитектуре;
5. Должны быть созданы индексы, ускоряющие запросы;
6. Должно применяться индексирования по полям, по которым будет производиться поиск;
7. При необходимости актуализируйте модель архитектуры в Structurizr DSL;
8. Ваши сервисы должны запускаться через docker-compose командой docker-compose up (создайте Docker файлы для каждого сервиса).

## Реализация

В данной лабораторной работе я выбрал сервис услуг для переноса данных из локального хранилища в noSQL MongoDB 5.0.

### Структура проекта

```
lab04/
├── docker-compose.yml       # Конфигурация
├── user-service/            # Сервис пользователей (работает с PostgreSQL) - остался без изменений.
└── service-service/         # Сервис услуг (MongoDB)
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py              # Основной файл приложения
    ├── database.py          # Подключение к MongoDB
    ├── auth.py              # Авторизация
    ├── seed.py              # Скрипт наполнения данными
    ├── models/              # Модели данных
    │   ├── __init__.py
    │   └── service.py       # Модель услуги
    └── routes/              # Маршруты API
        ├── __init__.py
        └── service_router.py # Маршруты для работы с услугами
```

### Особенности реализации

1. **MongoDB**: Использована MongoDB версии 5.0 для хранения данных о услугах.
2. **Индексы**: Созданы индексы по полям, по которым осуществляется поиск:
   - `category` - для фильтрации по категории услуг
   - `specialist_id` - для получения услуг конкретного специалиста
   - Текстовый индекс по полям `name` и `description` для текстового поиска
3. **Скрипт для наполнения данными**: Создан скрипт `seed.py`, который заполняет базу данных тестовыми значениями при первом запуске.
4. **CRUD операции**: Реализованы все необходимые операции для работы с услугами:
   - Create: `POST /api/services/`
   - Read: `GET /api/services/`, `GET /api/services/{service_id}`, `GET /api/services/specialist/{specialist_id}`
   - Update: `PUT /api/services/{service_id}`
   - Delete: `DELETE /api/services/{service_id}`
5. **Docker**: Настроен Docker Compose для запуска всех сервисов, включая MongoDB.

### Запуск проекта

Для запуска проекта выполните:

```bash
docker-compose up
```

Сервисы будут доступны по адресам:
- User Service: http://localhost:8000
- Service Service: http://localhost:8001

### API Documentation

API документация доступна по адресу:
- User Service: http://localhost:8000/docs
- Service Service: http://localhost:8001/docs 