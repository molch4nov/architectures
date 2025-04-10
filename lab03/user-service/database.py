import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from uuid import uuid4
from models.user import Base, UserORM, UserType

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/user_service_db")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    return pwd_context.verify(plain_password, hashed_password)

def init_db():
    """Initialize the database with tables and test data if it doesn't exist"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(UserORM).count() == 0:
            admin = UserORM(
                id=uuid4(),
                email="admin",
                first_name="Admin",
                last_name="User",
                phone="123456789",
                type=UserType.admin,
                password=hash_password("secret")
            )
            
            specialist = UserORM(
                id=uuid4(),
                email="specialist@example.com",
                first_name="Test",
                last_name="Specialist",
                phone="987654321",
                type=UserType.specialist,
                password=hash_password("password123")
            )

            customer = UserORM(
                id=uuid4(),
                email="customer@example.com",
                first_name="Test",
                last_name="Customer",
                phone="555555555",
                type=UserType.customer,
                password=hash_password("password123")
            )
            
            db.add_all([admin, specialist, customer])
            db.commit()
            print("Database initialized with test data")
        else:
            print("Database already has data, skipping initialization")
    finally:
        db.close() 