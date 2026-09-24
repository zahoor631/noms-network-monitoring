from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "noms_db"
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"

    # JWT
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"

    # Monitoring
    PING_INTERVAL: int = 60
    PING_TIMEOUT: int = 2
    ALERT_CPU_THRESHOLD: float = 85.0
    ALERT_MEMORY_THRESHOLD: float = 85.0
    ALERT_PACKET_LOSS_THRESHOLD: float = 10.0

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()