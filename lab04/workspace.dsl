workspace {
    name "Сервис бытовых услуг"
    description "Архитектура системы бытовых услуг"

    model {
        // Пользователи системы
        client = person "Клиент" "Пользователь, который заказывает услуги"
        specialist = person "Специалист" "Пользователь, который оказывает услуги" 
        administrator = person "Администратор" "Пользователь, который управляет системой"

        // Внешние системы
        paymentSystem = softwareSystem "Платежная система" "Внешняя система для обработки платежей"
        notificationSystem = softwareSystem "Система уведомлений" "Внешняя система для отправки уведомлений"

        // Основная система
        serviceSystem = softwareSystem "Сервис бытовых услуг" {
            // Фронтенд
            webApp = container "Веб-приложение" "Предоставляет функциональность для взаимодействия пользователей с системой" "React/TypeScript" {
                adminPanel = component "Панель администратора" "Интерфейс для управления системой"
                clientPanel = component "Панель клиента" "Интерфейс для заказа услуг"
                specialistPanel = component "Панель специалиста" "Интерфейс для управления оказываемыми услугами"
            }
            
            mobileApp = container "Мобильное приложение" "Мобильный интерфейс для клиентов и специалистов" "React Native" {
                // Компоненты мобильного приложения
            }

            // Бэкенд сервисы
            apiGateway = container "API Gateway" "Обеспечивает единую точку входа для всех клиентских приложений" "Express.js" {
                authMiddleware = component "Middleware авторизации" "Проверяет валидность токенов и права доступа"
                routingComponent = component "Компонент маршрутизации" "Направляет запросы в соответствующие микросервисы"
                loggingComponent = component "Компонент логирования" "Логирует все запросы и ошибки"
            }

            userService = container "Сервис пользователей" "Управление пользователями, аутентификация и авторизация" "FastAPI" {
                userController = component "Контроллер пользователей" "API для управления пользователями"
                authController = component "Контроллер авторизации" "API для аутентификации и авторизации"
                userModel = component "Модель пользователя" "Бизнес-логика работы с пользователями"
                tokenService = component "Сервис токенов" "Генерация и валидация JWT токенов"
            }

            serviceService = container "Сервис услуг" "Управление услугами и категориями" "FastAPI" {
                serviceController = component "Контроллер услуг" "API для управления услугами"
                serviceModel = component "Модель услуги" "Бизнес-логика работы с услугами"
                categoryModel = component "Модель категории" "Бизнес-логика работы с категориями"
                serviceCRUD = component "CRUD операции для услуг" "Реализация CRUD операций для услуг в MongoDB"
            }

            orderService = container "Сервис заказов" "Управление заказами" "FastAPI" {
                orderController = component "Контроллер заказов" "API для управления заказами"
                orderModel = component "Модель заказа" "Бизнес-логика работы с заказами"
                orderStatusService = component "Сервис статусов заказов" "Управление жизненным циклом заказов"
            }

            paymentService = container "Сервис платежей" "Обработка платежей" "FastAPI" {
                paymentController = component "Контроллер платежей" "API для управления платежами"
                paymentModel = component "Модель платежа" "Бизнес-логика работы с платежами"
                paymentGateway = component "Шлюз платежей" "Интеграция с внешней платежной системой"
            }

            notificationService = container "Сервис уведомлений" "Отправка уведомлений" "FastAPI" {
                notificationController = component "Контроллер уведомлений" "API для управления уведомлениями"
                notificationModel = component "Модель уведомления" "Бизнес-логика работы с уведомлениями"
                notificationGateway = component "Шлюз уведомлений" "Интеграция с внешней системой уведомлений"
            }

            // Базы данных
            userDB = container "База данных пользователей" "Хранит информацию о пользователях" "PostgreSQL" {
                tables = component "Таблицы пользователей" "Структура базы данных пользователей"
            }
            
            servicesDB = container "База данных услуг" "Хранит информацию об услугах и категориях" "MongoDB" {
                collections = component "Коллекции услуг" "Структура базы данных услуг"
            }
            
            orderDB = container "База данных заказов" "Хранит информацию о заказах" "PostgreSQL" {
                orderTables = component "Таблицы заказов" "Структура базы данных заказов"
            }

            // Очереди сообщений
            messageQueue = container "Очередь сообщений" "Обеспечивает асинхронное взаимодействие между сервисами" "RabbitMQ" {
                notificationQueue = component "Очередь уведомлений" "Очередь для уведомлений"
                orderQueue = component "Очередь заказов" "Очередь для заказов"
                paymentQueue = component "Очередь платежей" "Очередь для платежей"
            }
        }

        // Отношения между людьми и системой
        client -> serviceSystem "Заказывает услуги, оплачивает заказы, оставляет отзывы"
        specialist -> serviceSystem "Предоставляет услуги, получает оплату, управляет расписанием"
        administrator -> serviceSystem "Управляет пользователями, услугами, разрешает споры"

        // Отношения с внешними системами
        serviceSystem -> paymentSystem "Обрабатывает платежи через"
        serviceSystem -> notificationSystem "Отправляет уведомления через"

        // Отношения между контейнерами
        webApp -> apiGateway "Отправляет запросы на" "JSON/HTTPS"
        mobileApp -> apiGateway "Отправляет запросы на" "JSON/HTTPS"
        
        apiGateway -> userService "Перенаправляет запросы на" "JSON/HTTPS"
        apiGateway -> serviceService "Перенаправляет запросы на" "JSON/HTTPS"
        apiGateway -> orderService "Перенаправляет запросы на" "JSON/HTTPS"
        apiGateway -> paymentService "Перенаправляет запросы на" "JSON/HTTPS"
        apiGateway -> notificationService "Перенаправляет запросы на" "JSON/HTTPS"
        
        userService -> userDB "Читает и записывает данные" "SQL"
        serviceService -> servicesDB "Читает и записывает данные" "MongoDB Query"
        orderService -> orderDB "Читает и записывает данные" "SQL"
        
        userService -> messageQueue "Публикует сообщения" "AMQP"
        serviceService -> messageQueue "Публикует сообщения" "AMQP"
        orderService -> messageQueue "Публикует сообщения" "AMQP"
        paymentService -> messageQueue "Публикует сообщения" "AMQP"
        
        notificationService -> messageQueue "Потребляет сообщения" "AMQP"
        paymentService -> paymentSystem "Отправляет запросы на" "API/HTTPS"
        notificationService -> notificationSystem "Отправляет запросы на" "API/HTTPS"
    }

    views {
        systemContext serviceSystem "SystemContext" {
            include *
            autoLayout
        }
        
        container serviceSystem "Containers" {
            include *
            autoLayout
        }
        
        component userService "UserServiceComponents" {
            include *
            autoLayout
        }
        
        component serviceService "ServiceServiceComponents" {
            include *
            autoLayout
        }
        
        component orderService "OrderServiceComponents" {
            include *
            autoLayout
        }
        
        component apiGateway "ApiGatewayComponents" {
            include *
            autoLayout
        }
        
        theme default
    }
} 