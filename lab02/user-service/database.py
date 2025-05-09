from uuid import UUID, uuid4
from models.user import UserType

users = {}

admin_id = uuid4()
users[admin_id] = {
    "id": admin_id,
    "email": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "phone": "123456789",
    "type": UserType.admin,
    "password": "secret"
}

specialist_id = uuid4()
users[specialist_id] = {
    "id": specialist_id,
    "email": "specialist@example.com",
    "first_name": "Test",
    "last_name": "Specialist",
    "phone": "987654321",
    "type": UserType.specialist,
    "password": "password123"
}

customer_id = uuid4()
users[customer_id] = {
    "id": customer_id,
    "email": "customer@example.com",
    "first_name": "Test",
    "last_name": "Customer",
    "phone": "555555555",
    "type": UserType.customer,
    "password": "password123"
} 