workspace {
    name "Сайт заказа услуг (аналог profi.ru)"
    description "Архитектура системы заказа услуг специалистов"
    !identifiers hierarchical

    model {
        # Определение ролей пользователей
        customer = person "Клиент" "Пользователь, который ищет и заказывает услуги специалистов"
        specialist = person "Специалист" "Пользователь, который предоставляет услуги"
        admin = person "Администратор" "Сотрудник компании, который управляет платформой"
        
        # Основная система
        profiSystem = softwareSystem "Платформа заказа услуг" "Позволяет клиентам находить и заказывать услуги специалистов" {
            # Контейнеры
            frontend = container "Web интерфейс" "Пользовательский интерфейс системы для работы через браузер" "SolidJS" "Web App" {
                loginComponent = component "Компонент авторизации" "Авторизация и регистрация пользователей"
                serviceSearchComponent = component "Компонент поиска услуг" "Поиск услуг по различным критериям"
                serviceDetailComponent = component "Компонент детализации услуги" "Просмотр детальной информации об услуге"
                orderComponent = component "Компонент заказа" "Создание и управление заказами"
                profileComponent = component "Компонент профиля" "Управление профилем пользователя"
            }
            
            # Микросервисы (lab02)
            userService = container "Сервис пользователей" "Управляет пользователями и аутентификацией" "FastAPI, Python" "Microservice" {
                userApiComponent = component "API пользователей" "Эндпоинты для управления пользователями"
                authComponent = component "Аутентификация" "JWT авторизация и аутентификация пользователей"
                userDatabase = component "БД пользователей" "Хранение данных о пользователях (в памяти)"
            }
            
            serviceService = container "Сервис услуг" "Управляет услугами" "FastAPI, Python" "Microservice" {
                serviceApiComponent = component "API услуг" "Эндпоинты для управления услугами"
                tokenValidator = component "Валидатор токенов" "Проверяет JWT токены через сервис пользователей"
                serviceDatabase = component "БД услуг" "Хранение данных об услугах (в памяти)"
            }
            
            # Связи между контейнерами
            frontend -> userService "Отправляет запросы авторизации и управления пользователями" "HTTP/JSON"
            frontend -> serviceService "Отправляет запросы управления услугами" "HTTP/JSON"
            
            # Связь между микросервисами
            serviceService -> userService "Проверяет JWT токены" "HTTP/JSON"
            
            # Связи между компонентами
            frontend.loginComponent -> userService.authComponent "Запрашивает токен авторизации" "HTTP/JSON"
            frontend.profileComponent -> userService.userApiComponent "Управляет данными пользователя" "HTTP/JSON"
            frontend.serviceSearchComponent -> serviceService.serviceApiComponent "Поиск услуг" "HTTP/JSON"
            frontend.serviceDetailComponent -> serviceService.serviceApiComponent "Получение данных услуги" "HTTP/JSON"
            frontend.orderComponent -> serviceService.serviceApiComponent "Управление заказами" "HTTP/JSON"
            
            serviceService.tokenValidator -> userService.authComponent "Валидирует JWT токены" "HTTP/JSON"
        }
        
        # Отношения между людьми и системами
        customer -> profiSystem "Ищет и заказывает услуги"
        specialist -> profiSystem "Предлагает услуги и выполняет заказы"
        admin -> profiSystem "Управляет платформой"
        
        # Отношения между людьми и контейнерами
        customer -> profiSystem.frontend "Использует для поиска и заказа услуг" "HTTPS"
        specialist -> profiSystem.frontend "Использует для предложения услуг и управления заказами" "HTTPS"
        admin -> profiSystem.frontend "Использует для администрирования системы" "HTTPS"
        
        # Среда развертывания
        deploymentEnvironment "Production" {
            deploymentNode "Frontend Servers" {
                technology "Nginx"
                containerInstance profiSystem.frontend
            }
            
            deploymentNode "Microservices" {
                technology "Docker"
                
                deploymentNode "User Service Container" {
                    technology "Python, FastAPI"
                    containerInstance profiSystem.userService
                }
                
                deploymentNode "Service Service Container" {
                    technology "Python, FastAPI"
                    containerInstance profiSystem.serviceService
                }
            }
        }
    }
    
    views {
        systemContext profiSystem "SystemContext" {
            include *
            autoLayout
        }
        
        container profiSystem "Containers" {
            include *
            autoLayout
        }
        
        component profiSystem.frontend "FrontendComponents" {
            include *
            autoLayout
        }
        
        component profiSystem.userService "UserServiceComponents" {
            include *
            autoLayout
        }
        
        component profiSystem.serviceService "ServiceServiceComponents" {
            include *
            autoLayout
        }
        
        # Динамическая диаграмма для авторизации и получения данных (JWT)
        dynamic profiSystem "Auth" "Процесс авторизации и получения защищенных данных с JWT" {
            customer -> profiSystem.frontend "1. Ввод логина и пароля"
            profiSystem.frontend -> profiSystem.userService "2. Запрос токена" "HTTP/JSON"
            profiSystem.userService -> profiSystem.frontend "3. Возвращает JWT токен"
            profiSystem.frontend -> profiSystem.serviceService "4. Запрос защищенных данных с токеном" "HTTP/JSON"
            profiSystem.serviceService -> profiSystem.userService "5. Проверка токена" "HTTP/JSON"
            profiSystem.serviceService -> profiSystem.frontend "6. Возвращает данные"
            autoLayout
        }
        
        deployment profiSystem "Production" {
            include *
            autoLayout
        }
        
        theme default
        
        styles {
            element "Person" {
                shape person
                background #08427b
                color #ffffff
            }
            element "Web App" {
                shape WebBrowser
            }
            element "Microservice" {
                shape Hexagon
                background #85bbf0
                color #000000
            }
        }
    }
} 