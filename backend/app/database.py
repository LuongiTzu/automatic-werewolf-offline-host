"""Database configuration"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Use SQLite for local development
# Format: sqlite:///./database.db (relative to backend directory)
database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///./werewolf.db"
)

# SQLite specific configuration
connect_args = {}
engine_kwargs = {}

if database_url.startswith("sqlite"):
    # SQLite requires check_same_thread=False for SQLAlchemy
    connect_args = {"check_same_thread": False}
    engine_kwargs = {"connect_args": connect_args}

engine = create_engine(
    database_url,
    echo=settings.DEBUG,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables in database"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
