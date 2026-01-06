import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import sessionmaker

load_dotenv()

# PostgreSQL connection (Defaulting to the Neon URL found in .env.local)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_5VxM3marKnbw@ep-wispy-mud-ab4bb57t-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create database tables based on SQLModel metadata"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for providing database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
