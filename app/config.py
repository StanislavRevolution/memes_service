from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    SECRET_KEY: str
    ALGORITHM: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    ACCESS_KEY: str
    SECRET_KEY: str
    ENDPOINT_URL: str
    BUCKET_NAME: str
    S3_IMAGE_PRE_LINK: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
