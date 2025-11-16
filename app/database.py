from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,      # shows SQL statements in console
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Base class for all ORM models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()