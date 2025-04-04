# Документация архитектуры сайта заказа услуг

## Обзор

Архитектура системы построена на компонентной модели с использованием следующего стека технологий:
- Frontend: SolidJS
- Backend: Express.js, Node.js
- Database: PostgreSQL (включая полнотекстовый поиск)

## Роли пользователей

1. **Клиент** - пользователь, который ищет и заказывает услуги специалистов
2. **Специалист** - пользователь, который предоставляет услуги
3. **Администратор** - сотрудник компании, который управляет платформой

## Основные компоненты системы

- **Web интерфейс** - пользовательский интерфейс для браузера на SolidJS
- **Сервис пользователей** - управление данными пользователей, аутентификация и авторизация
- **Сервис услуг** - управление каталогом услуг и их характеристиками
- **Сервис заказов** - управление заказами и их статусами
- **Сервис поиска** - обеспечивает поиск специалистов и услуг с использованием возможностей PostgreSQL
- **База данных** - PostgreSQL для хранения данных и выполнения поисковых запросов

## Ключевые бизнес-процессы

1. Регистрация пользователей (клиентов и специалистов)
2. Создание и управление каталогом услуг
3. Поиск специалистов и услуг по различным критериям
4. Создание заказов на услуги
5. Управление заказами

## Среда развертывания

Система развертывается в трех основных сегментах:
1. **Frontend Servers** - серверы с Nginx для обслуживания фронтенда
2. **Application Servers** - серверы с Node.js для запуска микросервисов
3. **Database Servers** - серверы с PostgreSQL для хранения данных 