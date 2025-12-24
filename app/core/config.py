from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "FastAPI Todo Backend"
    environment: str = Field(default="development")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()