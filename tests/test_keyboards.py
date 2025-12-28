"""Tests for keyboard builders."""
import pytest
from bot.keyboards.inline import (
    get_start_keyboard,
    get_link_keyboard,
    get_help_keyboard,
    is_valid_telegram_url,
)


def test_get_start_keyboard():
    """Test start keyboard has correct buttons."""
    keyboard = get_start_keyboard()

    assert keyboard is not None
    assert len(keyboard.inline_keyboard) == 2

    # First row - refresh status
    assert keyboard.inline_keyboard[0][0].callback_data == "refresh_status"

    # Second row - help
    assert keyboard.inline_keyboard[1][0].callback_data == "help"


def test_get_link_keyboard_with_valid_url():
    """Test link keyboard with valid https URL."""
    frontend_url = "https://omnimap.cloud.ru"
    telegram_id = 123456789

    keyboard = get_link_keyboard(frontend_url, telegram_id)

    assert keyboard is not None
    assert len(keyboard.inline_keyboard) == 2

    # First row - link button with URL
    link_button = keyboard.inline_keyboard[0][0]
    assert f"telegram?link={telegram_id}" in link_button.url
    assert frontend_url in link_button.url

    # Second row - help
    assert keyboard.inline_keyboard[1][0].callback_data == "help"


def test_get_link_keyboard_with_localhost():
    """Test link keyboard returns None for localhost URL."""
    frontend_url = "http://localhost:3000"
    telegram_id = 123456789

    keyboard = get_link_keyboard(frontend_url, telegram_id)

    assert keyboard is None


def test_get_link_keyboard_with_http():
    """Test link keyboard returns None for http URL."""
    frontend_url = "http://example.com"
    telegram_id = 123456789

    keyboard = get_link_keyboard(frontend_url, telegram_id)

    assert keyboard is None


def test_get_help_keyboard():
    """Test help keyboard has only help button."""
    keyboard = get_help_keyboard()

    assert keyboard is not None
    assert len(keyboard.inline_keyboard) == 1
    assert keyboard.inline_keyboard[0][0].callback_data == "help"


def test_is_valid_telegram_url():
    """Test URL validation for Telegram inline buttons."""
    assert is_valid_telegram_url("https://omnimap.cloud.ru") is True
    assert is_valid_telegram_url("https://example.com") is True
    assert is_valid_telegram_url("http://localhost:3000") is False
    assert is_valid_telegram_url("https://localhost:3000") is False
    assert is_valid_telegram_url("http://example.com") is False
