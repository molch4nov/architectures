# API системы заказа услуг

## API сервиса пользователей

### Управление пользователями (UserController)

#### 1. Создание нового пользователя
```
POST /api/users
Content-Type: application/json

{
  "type": "customer|specialist",
  "email": "string",
  "password": "string",
  "firstName": "string",
  "lastName": "string",
  "phone": "string"
}
```

#### 2. Поиск пользователя по логину (email)
```
GET /api/users?email=user@example.com
```

#### 3. Поиск пользователя по маске имени и фамилии
```
GET /api/users?name=Иван&lastName=Петров
```

### Аутентификация (AuthController)

#### 1. Вход в систему
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "string",
  "password": "string"
}
```

#### 2. Выход из системы
```
POST /api/auth/logout
```

## API сервиса услуг

### Управление услугами (ServiceController)

#### 1. Создание услуги
```
POST /api/services
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "category": "string",
  "price": number,
  "duration": number
}
```

#### 2. Получение списка услуг
```
GET /api/services
```
Опциональные параметры:
- category - фильтр по категории
- specialist - фильтр по ID специалиста
- minPrice/maxPrice - фильтр по диапазону цен

### Управление категориями (CategoryController)

#### 1. Получение списка категорий
```
GET /api/categories
```

## API сервиса заказов

### Управление заказами (OrderController)

#### 1. Создание заказа
```
POST /api/orders
Content-Type: application/json

{
  "userId": "string",
  "services": [
    { 
      "serviceId": "string",
      "quantity": number,
      "date": "string"
    }
  ]
}
```

#### 2. Получение заказа для пользователя
```
GET /api/orders?userId=userId
```

### Управление элементами заказа (OrderItemController)

#### 1. Добавление услуг в заказ
```
POST /api/orders/{orderId}/items
Content-Type: application/json

{
  "serviceId": "string",
  "quantity": number,
  "date": "string"
}
```

## API сервиса поиска

### Поиск (SearchController)

#### 1. Полнотекстовый поиск услуг
```
GET /api/search/services?query=string
```
Опциональные параметры:
- category - фильтр по категории
- minPrice/maxPrice - фильтр по диапазону цен
- sort - сортировка результатов (relevance, price_asc, price_desc)
- limit - ограничение количества результатов
- offset - смещение для пагинации

#### 2. Поиск специалистов
```
GET /api/search/specialists?query=string
```
Опциональные параметры:
- experience - минимальный опыт работы
- rating - минимальный рейтинг
- sort - сортировка результатов (relevance, rating, experience)
- limit - ограничение количества результатов
- offset - смещение для пагинации 