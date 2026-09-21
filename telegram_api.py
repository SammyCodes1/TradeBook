"""Telegram Bot API communication for TradeBook."""

import logging
import httpx
from config import TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)

# One module-level httpx client
_client = httpx.Client(timeout=10.0)
_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_message(chat_id: int, text: str) -> bool:
    """Send a plain text message to a Telegram chat. Never raises."""
    try:
        response = _client.post(
            _API_URL,
            json={"chat_id": chat_id, "text": text},
        )
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            description = data.get("description", "Unknown error")
            logger.error(
                "Telegram API error: status=%s, description=%s",
                response.status_code,
                description,
            )
            return False
        return True
    except httpx.HTTPStatusError as exc:
        description = "Unknown error"
        try:
            description = exc.response.json().get("description", description)
        except Exception:
            pass
        logger.error(
            "Telegram HTTP error: status=%s, description=%s",
            exc.response.status_code,
            description,
        )
        return False
    except httpx.HTTPError:
        logger.error("Telegram network error")
        return False
    except Exception:
        logger.error("Unexpected error sending Telegram message")
        return False
