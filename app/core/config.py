from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"

    PROJECT_NAME: str
    MONGO_SERVER: str
    MONGO_PORT: int = 27017
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DB: str

    @computed_field
    @property
    def MONGO_CONNECTION_STRING(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_SERVER}:{self.MONGO_PORT}/{self.MONGO_DB}?authSource=admin"


settings = Settings()
