from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Setting Configuration."""

    API_V1_STR: str = "/api"

    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_USER: str
    DB_PASSWORD: str

    ALPACA_API_KEY_ID: str
    ALPACA_API_SECRET_KEY: str
    ALPACA_BASE_URL: str
    
    class Config:
        case_sensitive = False
        env_file = Path(__file__).parent / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
