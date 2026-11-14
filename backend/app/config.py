from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./home_central.db"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Stand-in identity until real auth arrives (Milestone 10).
    dev_user_email: str = "dev@home-central.local"
    dev_user_display_name: str = "Dev User"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
