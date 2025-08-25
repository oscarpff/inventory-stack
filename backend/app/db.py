from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/inventory"
    CORS_ORIGINS: str = "http://localhost:5173"
    JWT_SECRET: str = "devsecret"
    JWT_ALGO: str = "HS256"

settings = Settings(_env_file=os.getenv("ENV_FILE", ".env"), _env_file_encoding="utf-8")

engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()
