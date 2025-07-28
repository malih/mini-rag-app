from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: List[str] = []
    FILE_MAX_SIZE: int = 0
    FILE_DEFAULT_CHUNK_SIZE: int = 0
    PROJECTS_DIR: str

    MONGODB_URL: str
    MONGODB_DATABASE: str

    class Config:
        env_file = "src/.env"

def get_settings():
    return Settings()