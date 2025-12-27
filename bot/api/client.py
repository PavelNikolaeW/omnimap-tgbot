"""HTTP client for OmniMap backend API."""
import logging
from typing import Optional

import httpx

from bot.config import settings

logger = logging.getLogger(__name__)


class OmniMapClient:
    """Client for OmniMap backend API."""

    def __init__(self) -> None:
        self.base_url = settings.omnimap_backend_url
        self.secret = settings.telegram_bot_secret
        self.timeout = httpx.Timeout(10.0)

    def _get_headers(self) -> dict:
        """Get headers with authentication."""
        return {
            "X-Bot-Secret": self.secret,
            "Content-Type": "application/json",
        }

    async def check_user_linked(self, telegram_id: int) -> bool:
        """Check if Telegram user is linked to OmniMap account."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/telegram/check/{telegram_id}/",
                    headers=self._get_headers(),
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("linked", False)
                return False
        except Exception as e:
            logger.error(f"Error checking user link status: {e}")
            return False

    async def unlink_user(self, telegram_id: int) -> bool:
        """Unlink Telegram user from OmniMap account."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/telegram/unlink/",
                    headers=self._get_headers(),
                    json={"telegram_id": telegram_id},
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error unlinking user: {e}")
            return False

    async def get_user_info(self, telegram_id: int) -> Optional[dict]:
        """Get linked OmniMap user info."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/telegram/user/{telegram_id}/",
                    headers=self._get_headers(),
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None
