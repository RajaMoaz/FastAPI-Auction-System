# File: database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm import Session
from typing import Generator
import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
# This looks for the .env file and loads the variables.
load_dotenv()

# --- PRODUCTION CONFIGURATION: PostgreSQL ---
# IMPORTANT: Instruct your professor to update these values to their local setup.

# os.getenv('VARIABLE_NAME', 'Default_Value') 
# Fetches value from .env, or uses the second argument as a default (for your prof)
POSTGRES_USER = os.getenv("POSTGRES_USER", "YOUR_PROF_USER") 
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "YOUR_PROF_PASS") 
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost") 
POSTGRES_DB = os.getenv("POSTGRES_DB", "auction_db") 

# 1. Database Configuration
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)
# create_engine is the starting point for SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # NOTE: The 'connect_args={"check_same_thread": False}' argument is
    # REMOVED because it is only required for the SQLite driver.
)

# 2. Session Factory
# SessionLocal will be used to create a database session for each request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base Class for Models
# This is the base class that all your model classes will inherit from in models.py.
class Base(DeclarativeBase):
    pass

# Helper function (Dependency) to get a database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()