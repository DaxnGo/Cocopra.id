import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for local MVP, easily swappable to PostgreSQL later
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cocopra.db")

# SQLite needs connect_args={"check_same_thread": False}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
