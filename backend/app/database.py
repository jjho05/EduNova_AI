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
            "pool_recycle": 300,
            "pool_size": 3,
            "max_overflow": 5,
            "connect_args": {
                "options": "-c statement_timeout=60000",
            },
        }
    )

# Supabase Pooler requires prepared_statements=false in the URL
db_url = settings.DATABASE_URL
if "pooler.supabase.com" in db_url and "prepared_statements" not in db_url:
    separator = "&" if "?" in db_url else "?"
    db_url = f"{db_url}{separator}prepared_statements=false"

engine = create_engine(db_url, **engine_kwargs)

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
