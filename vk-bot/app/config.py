from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    vk_token: str
    api_base: str = "http://localhost:8000"

    chat_broadcast_interval_seconds: int = 86400
    wall_post_interval_seconds: int = 600
