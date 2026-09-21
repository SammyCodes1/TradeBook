"""FastAPI webhook application for TradeBook."""

import hmac
import logging
from fastapi import FastAPI, Header, HTTPException, Body
from config import WEBHOOK_SECRET
import handlers
import telegram_api

# Setup logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "app": "TradeBook"}


@app.post("/webhook")
def webhook(
    x_telegram_bot_api_secret_token: str | None = Header(None),
    update: dict = Body(default_factory=dict),
):
    """Telegram webhook endpoint."""
    # Secret token check
    if not x_telegram_bot_api_secret_token or not hmac.compare_digest(
        x_telegram_bot_api_secret_token, WEBHOOK_SECRET
    ):
        raise HTTPException(status_code=403, detail="Forbidden")

    chat_id = None
    try:
        # Ignore updates without a message
        message = update.get("message")
        if not message or not isinstance(message, dict):
            return {"ok": True}

        # Ignore messages from bots
        from_user = message.get("from") or {}
        if from_user.get("is_bot"):
            return {"ok": True}

        chat = message.get("chat") or {}
        chat_id = chat.get("id")
        if chat_id is None:
            return {"ok": True}

        trader_id = from_user.get("id")
        if trader_id is None:
            trader_id = chat_id

        update_id = update.get("update_id", 0)

        # Require text in the message
        text = message.get("text")
        if not text:
            telegram_api.send_message(
                chat_id, "Please send text like: sold 3 rice 15000"
            )
            return {"ok": True}

        # Process text and send reply
        reply = handlers.handle_text(trader_id, update_id, text)
        if reply is not None:
            telegram_api.send_message(chat_id, reply)

    except Exception:
        logger.exception("Error processing update_id=%s", update.get("update_id"))
        if chat_id is not None:
            try:
                telegram_api.send_message(
                    chat_id,
                    "Sorry, something went wrong. Please try again in a minute.",
                )
            except Exception:
                pass

    return {"ok": True}
