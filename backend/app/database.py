from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Global flag to track if we fell back to SQLite
IS_DATABASE_FALLBACK = False

# Create engine
engine_kwargs = {"echo": False}
DATABASE_URL = settings.DATABASE_URL

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update(
        {
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "pool_size": 3,
            "max_overflow": 5,
        }
    )

try:
    # Attempt to connect to the configured database
    engine = create_engine(DATABASE_URL, **engine_kwargs)
    if not DATABASE_URL.startswith("sqlite"):
        # Test connection immediately
        with engine.connect() as conn:
            pass
    print("✅ Conexión a base de datos principal exitosa.")
except Exception as e:
    print(f"⚠️ Error al conectar a la base de datos principal: {e}")
    print("🔄 Cayendo en base de datos SQLite local de respaldo...")
    IS_DATABASE_FALLBACK = True
    DATABASE_URL = "sqlite:///./educativo_fallback.db"
    engine_kwargs = {"connect_args": {"check_same_thread": False}}
    engine = create_engine(DATABASE_URL, **engine_kwargs)

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
