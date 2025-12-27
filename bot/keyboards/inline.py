"""Inline keyboard builders."""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for linked users."""
    keyboard = [
        [InlineKeyboardButton("🔄 Обновить статус", callback_data="refresh_status")],
        [InlineKeyboardButton("📚 Справка", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_link_keyboard(frontend_url: str, telegram_id: int) -> InlineKeyboardMarkup:
    """Get keyboard with link to connect account."""
    link_url = f"{frontend_url}/settings/telegram?link={telegram_id}"
    keyboard = [
        [InlineKeyboardButton("🔗 Привязать аккаунт", url=link_url)],
        [InlineKeyboardButton("📚 Справка", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)
