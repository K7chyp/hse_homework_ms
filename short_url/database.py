from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Настройки PostgreSQL
POSTGRES_USER = "user"
POSTGRES_PASSWORD = "password"
POSTGRES_DB = "app_db"
POSTGRES_HOST = "db_container"
POSTGRES_PORT = "5432"

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
