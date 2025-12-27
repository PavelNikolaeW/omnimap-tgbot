"""Bot configuration from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Bot settings loaded from environment."""

    # Telegram
    telegram_bot_token: str
    telegram_bot_secret: str = ""

    # Backend API
    omnimap_backend_url: str = "http://omnimap-back:8000"

    # Frontend URL
    frontend_url: str = "http://localhost:3000"

    # Webhook settings
    webhook_url: str = ""
    webhook_port: int = 8002

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
