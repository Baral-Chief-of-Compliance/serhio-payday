from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgresuser"
    postgres_password: str = ""
    postgres_db: str = "SERHIO_PAYDAY"

    start_balance: float = 100_000.0
    tick_min_seconds: float = 3.0
    tick_max_seconds: float = 4.0
    income_probability: float = 0.75

    income_data_path: Path = DATA_DIR / "income.json"
    expenses_data_path: Path = DATA_DIR / "expenses.json"

    centrifugo_enabled: bool = False
    centrifugo_api_url: str = "http://localhost:7000/api"
    centrifugo_api_key: str = ""
    centrifugo_channel: str = "serhio_payday:ticks"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
