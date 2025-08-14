from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    PROJECT_NAME: str
    MONGO_SERVER: str
    MONGO_PORT: int = 27017
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DB: str

    @computed_field
    @property
    def MONGO_CONNECTION_STRING(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_SERVER}:{self.MONGO_PORT}/{self.MONGO_DB}"


settings = Settings()
