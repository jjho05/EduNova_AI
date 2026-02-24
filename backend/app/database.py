from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create engine
engine_kwargs = {"echo": False}

if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update(
        {
            "pool_pre_ping": True,
            "pool_recycle": 3600,
            "pool_size": 10,
            "max_overflow": 20,
        }
    )

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
