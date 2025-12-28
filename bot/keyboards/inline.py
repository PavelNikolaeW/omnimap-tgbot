"""Inline keyboard builders."""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for linked users."""
    keyboard = [
        [InlineKeyboardButton("🔄 Обновить статус", callback_data="refresh_status")],
        [InlineKeyboardButton("📚 Справка", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def is_valid_telegram_url(url: str) -> bool:
    """Check if URL is valid for Telegram inline buttons (must be https, no localhost)."""
    return url.startswith("https://") and "localhost" not in url


def get_link_keyboard(frontend_url: str, telegram_id: int) -> InlineKeyboardMarkup | None:
    """Get keyboard with link to connect account.

    Returns None if the URL is not valid for Telegram (e.g., localhost in dev).
    """
    link_url = f"{frontend_url}/settings/telegram?link={telegram_id}"

    if not is_valid_telegram_url(frontend_url):
        return None

    keyboard = [
        [InlineKeyboardButton("🔗 Привязать аккаунт", url=link_url)],
        [InlineKeyboardButton("📚 Справка", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_help_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard with help button only."""
    keyboard = [
        [InlineKeyboardButton("📚 Справка", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)
