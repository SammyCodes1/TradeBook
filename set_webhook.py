"""Register the webhook with Telegram."""

import os
import sys
from dotenv import load_dotenv
import httpx

# Load environment variables without importing config.py
load_dotenv()


def main():
    raw_token = os.getenv("TELEGRAM_BOT_TOKEN")
    token = raw_token.strip() if raw_token else ""

    raw_secret = os.getenv("WEBHOOK_SECRET")
    secret = raw_secret.strip() if raw_secret else ""

    raw_url = os.getenv("PUBLIC_URL")
    public_url = raw_url.strip() if raw_url else ""

    missing = []
    if not token:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not secret:
        missing.append("WEBHOOK_SECRET")
    if not public_url:
        missing.append("PUBLIC_URL")

    if missing:
        print(f"Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

    if not public_url.startswith("https://"):
        print("Error: PUBLIC_URL must start with https://")
        sys.exit(1)

    public_url = public_url.rstrip("/")
    webhook_url = f"{public_url}/webhook"

    base_url = f"https://api.telegram.org/bot{token}"
    payload = {
        "url": webhook_url,
        "secret_token": secret,
        "allowed_updates": ["message"],
        "drop_pending_updates": True,
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(f"{base_url}/setWebhook", json=payload)
            data = resp.json()
            print(f"ok: {data.get('ok')}")
            print(f"description: {data.get('description')}")

            resp_info = client.get(f"{base_url}/getWebhookInfo")
            info_data = resp_info.json()
            result = info_data.get("result", {})
            print(f"url: {result.get('url')}")
            print(f"pending_update_count: {result.get('pending_update_count')}")
            print(f"last_error_date: {result.get('last_error_date')}")
            print(f"last_error_message: {result.get('last_error_message')}")

    except httpx.HTTPStatusError as exc:
        print(f"HTTP error: status={exc.response.status_code}")
        try:
            err_data = exc.response.json()
            print(f"description: {err_data.get('description')}")
        except Exception:
            pass
        sys.exit(1)
    except httpx.HTTPError:
        print("Network error connecting to Telegram API")
        sys.exit(1)


if __name__ == "__main__":
    main()
