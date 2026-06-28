from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "NovaShell"
    DATABASE_URL: str = "postgresql+asyncpg://novashell:password@localhost:5433/novashell_db"
    REDIS_URL: str = "redis://localhost:6380/0"
    SECRET_KEY: str = "super_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
