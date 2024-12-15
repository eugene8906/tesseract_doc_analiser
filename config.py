import os
import sys
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    ALLOWED_HOSTS: str | None = None

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')


settings = Settings()

