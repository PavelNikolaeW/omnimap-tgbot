"""Start, status, and unlink command handlers."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.api.client import OmniMapClient
from bot.config import settings
from bot.keyboards.inline import get_start_keyboard, get_link_keyboard

logger = logging.getLogger(__name__)
client = OmniMapClient()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")

    # Check if user is already linked
    is_linked = await client.check_user_linked(user.id)

    if is_linked:
        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n\n"
            f"Ваш Telegram аккаунт уже привязан к OmniMap.\n"
            f"Вы будете получать уведомления о важных событиях.\n\n"
            f"Команды:\n"
            f"/status — проверить статус привязки\n"
            f"/unlink — отвязать аккаунт",
            reply_markup=get_start_keyboard(),
        )
    else:
        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n\n"
            f"Я бот OmniMap для получения уведомлений.\n\n"
            f"Чтобы привязать аккаунт, нажмите кнопку ниже "
            f"или перейдите в настройки профиля на сайте.",
            reply_markup=get_link_keyboard(settings.frontend_url, user.id),
        )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    user = update.effective_user

    is_linked = await client.check_user_linked(user.id)

    if is_linked:
        await update.message.reply_text(
            "✅ Ваш аккаунт привязан к OmniMap.\n\n"
            "Вы получаете уведомления о:\n"
            "• Изменениях в общих проектах\n"
            "• Комментариях и упоминаниях\n"
            "• Важных системных событиях",
        )
    else:
        await update.message.reply_text(
            "❌ Ваш аккаунт не привязан к OmniMap.\n\n"
            "Используйте /start для привязки.",
        )


async def unlink_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /unlink command."""
    user = update.effective_user

    is_linked = await client.check_user_linked(user.id)

    if not is_linked:
        await update.message.reply_text(
            "Ваш аккаунт не привязан к OmniMap.",
        )
        return

    success = await client.unlink_user(user.id)

    if success:
        await update.message.reply_text(
            "✅ Аккаунт успешно отвязан.\n\n"
            "Вы больше не будете получать уведомления.\n"
            "Используйте /start для повторной привязки.",
        )
    else:
        await update.message.reply_text(
            "❌ Не удалось отвязать аккаунт.\n\n"
            "Попробуйте позже или обратитесь в поддержку.",
        )
