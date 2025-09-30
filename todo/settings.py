from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str
    api_url: str
    api_port: str
    db_url: str
    db_port: str

settings = Settings()
