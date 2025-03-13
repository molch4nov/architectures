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
            
            userService = container "Сервис пользователей" "Управляет данными пользователей, аутентификацией и авторизацией" "Express.js, Node.js" "Service" {
                userController = component "Контроллер пользователей" "API для работы с пользователями"
                authController = component "Контроллер авторизации" "API для авторизации и аутентификации"
                userRepository = component "Репозиторий пользователей" "Доступ к данным пользователей"
            }
            
            serviceService = container "Сервис услуг" "Управляет каталогом услуг и их характеристиками" "Express.js, Node.js" "Service" {
                serviceController = component "Контроллер услуг" "API для работы с услугами"
                serviceRepository = component "Репозиторий услуг" "Доступ к данным услуг"
                categoryController = component "Контроллер категорий" "API для работы с категориями услуг"
            }
            
            orderService = container "Сервис заказов" "Управляет заказами и их статусами" "Express.js, Node.js" "Service" {
                orderController = component "Контроллер заказов" "API для работы с заказами"
                orderRepository = component "Репозиторий заказов" "Доступ к данным заказов"
                orderItemController = component "Контроллер элементов заказа" "API для работы с элементами заказа"
            }
            
            searchService = container "Сервис поиска" "Обеспечивает поиск специалистов и услуг по различным критериям" "Express.js, Node.js" "Service" {
                searchController = component "Контроллер поиска" "API для поиска"
                searchQueryBuilder = component "Построитель поисковых запросов" "Формирует SQL-запросы для поиска"
            }
            
            # База данных
            database = container "База данных" "Хранит данные о пользователях, услугах и заказах" "PostgreSQL" "Database"
            
            # Связи между контейнерами
            frontend -> userService "Отправляет запросы пользовательских операций" "HTTP/JSON"
            frontend -> serviceService "Отправляет запросы управления услугами" "HTTP/JSON"
            frontend -> orderService "Отправляет запросы управления заказами" "HTTP/JSON"
            frontend -> searchService "Отправляет поисковые запросы" "HTTP/JSON"
            
            userService -> database "Читает и записывает данные пользователей" "SQL/TCP"
            serviceService -> database "Читает и записывает данные услуг" "SQL/TCP"
            orderService -> database "Читает и записывает данные заказов" "SQL/TCP"
            searchService -> database "Выполняет поисковые запросы" "SQL/TCP"
            
            # Связи между компонентами
            frontend.loginComponent -> userService.authController "Авторизация пользователя" "HTTP/JSON"
            frontend.profileComponent -> userService.userController "Управление профилем" "HTTP/JSON"
            frontend.serviceSearchComponent -> searchService.searchController "Поиск услуг" "HTTP/JSON"
            frontend.serviceDetailComponent -> serviceService.serviceController "Получение данных услуги" "HTTP/JSON"
            frontend.orderComponent -> orderService.orderController "Управление заказами" "HTTP/JSON"
            
            searchService.searchController -> searchService.searchQueryBuilder "Формирует поисковый запрос"
            searchService.searchQueryBuilder -> database "Выполняет поисковый запрос" "SQL/TCP"
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
            
            deploymentNode "Application Servers" {
                technology "Node.js"
                containerInstance profiSystem.userService
                containerInstance profiSystem.serviceService
                containerInstance profiSystem.orderService
                containerInstance profiSystem.searchService
            }
            
            deploymentNode "Database Servers" {
                technology "PostgreSQL"
                containerInstance profiSystem.database
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
        
        component profiSystem.serviceService "ServiceComponents" {
            include *
            autoLayout
        }
        
        component profiSystem.orderService "OrderComponents" {
            include *
            autoLayout
        }
        
        component profiSystem.searchService "SearchComponents" {
            include *
            autoLayout
        }
        
        # Динамическая диаграмма для создания заказа
        dynamic profiSystem "CreateOrder" "Процесс создания заказа на услугу" {
            customer -> profiSystem.frontend "1. Выбирает услугу и переходит к созданию заказа"
            profiSystem.frontend -> profiSystem.searchService "2. Поиск услуги" "HTTP/JSON"
            profiSystem.searchService -> profiSystem.database "3. Выполняет поисковый запрос" "SQL/TCP"
            profiSystem.frontend -> profiSystem.serviceService "4. Запрос деталей услуги" "HTTP/JSON"
            profiSystem.frontend -> profiSystem.orderService "5. Создание заказа" "HTTP/JSON"
            profiSystem.orderService -> profiSystem.database "6. Сохранение данных заказа" "SQL/TCP"
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
            element "Database" {
                shape Cylinder
            }
            element "Service" {
                shape Hexagon
            }
        }
    }
} 