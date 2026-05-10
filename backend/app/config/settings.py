from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./educativo.db"
    
    # Gemini API
    GEMINI_API_KEY: str = "dummy_key_for_startup"
    
    # JWT
    SECRET_KEY: str = "test_secret_key_change_me_in_prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "*"  # Default to all for development, override in prod
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra env vars

settings = Settings()
