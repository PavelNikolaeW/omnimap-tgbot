"""Tests for bot configuration."""
import os
import pytest


def test_settings_from_env(monkeypatch):
    """Test that settings load from environment variables."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token_123")
    monkeypatch.setenv("TELEGRAM_BOT_SECRET", "test_secret")
    monkeypatch.setenv("OMNIMAP_BACKEND_URL", "http://test-backend:8000")
    monkeypatch.setenv("FRONTEND_URL", "http://test-frontend:3000")

    # Re-import to pick up new env vars
    from bot.config import Settings
    settings = Settings()

    assert settings.telegram_bot_token == "test_token_123"
    assert settings.telegram_bot_secret == "test_secret"
    assert settings.omnimap_backend_url == "http://test-backend:8000"
    assert settings.frontend_url == "http://test-frontend:3000"


def test_settings_defaults(monkeypatch):
    """Test default values for optional settings."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")

    from bot.config import Settings
    settings = Settings()

    assert settings.webhook_port == 8002
    assert settings.log_level == "INFO"
    assert settings.webhook_url == ""
