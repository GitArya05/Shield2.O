from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# pool_pre_ping=True is crucial. It tests the connection before using it.
# If the serverless database went to sleep, this wakes it up safely.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, 
    pool_size=5,
    max_overflow=10
)

# This creates isolated database sessions for every API request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to inject the database session into our routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()