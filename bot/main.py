"""Main entry point for the OmniMap Telegram Bot."""
import asyncio
import logging

from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler

from bot.config import settings
from bot.handlers.start import start_command, status_command, unlink_command
from bot.handlers.callbacks import button_callback

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.log_level.upper()),
)
logger = logging.getLogger(__name__)


async def health_check(request: web.Request) -> web.Response:
    """Health check endpoint."""
    return web.json_response({"status": "ok"})


async def run_health_server() -> None:
    """Run health check HTTP server."""
    app = web.Application()
    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", settings.webhook_port)
    await site.start()
    logger.info(f"Health server started on port {settings.webhook_port}")


def create_application() -> Application:
    """Create and configure the bot application."""
    application = Application.builder().token(settings.telegram_bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("unlink", unlink_command))

    # Add callback query handler
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(button_callback))

    return application


async def main() -> None:
    """Main function to run the bot."""
    logger.info("Starting OmniMap Telegram Bot...")

    # Start health check server
    await run_health_server()

    # Create application
    application = create_application()

    if settings.webhook_url:
        # Webhook mode (production)
        logger.info(f"Running in webhook mode: {settings.webhook_url}")
        await application.run_webhook(
            listen="0.0.0.0",
            port=settings.webhook_port,
            url_path="/webhook",
            webhook_url=f"{settings.webhook_url}/webhook",
        )
    else:
        # Polling mode (development)
        logger.info("Running in polling mode")
        await application.initialize()
        await application.start()
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

        # Keep running
        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Stopping bot...")
        finally:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
