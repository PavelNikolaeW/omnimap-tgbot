"""Inline button callback handlers."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button callbacks."""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "refresh_status":
        from bot.handlers.start import status_command
        # Create a fake message update for status command
        await status_command(update, context)
    elif data == "help":
        await query.edit_message_text(
            "📚 Справка по боту OmniMap\n\n"
            "Команды:\n"
            "/start — начать работу с ботом\n"
            "/status — проверить статус привязки\n"
            "/unlink — отвязать аккаунт\n\n"
            "Бот отправляет уведомления о:\n"
            "• Изменениях в общих проектах\n"
            "• Комментариях и упоминаниях\n"
            "• Важных системных событиях",
        )
    else:
        logger.warning(f"Unknown callback data: {data}")
