"""Tests for keyboard builders."""
import pytest
from bot.keyboards.inline import get_start_keyboard, get_link_keyboard


def test_get_start_keyboard():
    """Test start keyboard has correct buttons."""
    keyboard = get_start_keyboard()

    assert keyboard is not None
    assert len(keyboard.inline_keyboard) == 2

    # First row - refresh status
    assert keyboard.inline_keyboard[0][0].callback_data == "refresh_status"

    # Second row - help
    assert keyboard.inline_keyboard[1][0].callback_data == "help"


def test_get_link_keyboard():
    """Test link keyboard contains correct URL."""
    frontend_url = "http://localhost:3000"
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
