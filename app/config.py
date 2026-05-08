from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASS : str
    DB_NAME : str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    REDIS_DB_HOST  : str
    REDIS_DB_PORT : int

    @property
    def REDIS_DB_URL(self):
        return f"redis://{self.REDIS_DB_HOST}:{self.REDIS_DB_PORT}"
    
    RABBITMQ_HOST : str
    RABBITMQ_PORT : int

    @property
    def RABBIT_URL(self):
        return f"amqp://guest:guest@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()

