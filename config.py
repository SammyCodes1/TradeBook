import os
from dotenv import load_dotenv

# Load local environment variables without overriding existing ones
load_dotenv()

_missing = []

# Read and validate required environment variables
_raw_telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = _raw_telegram_token.strip() if _raw_telegram_token is not None else ""
if not TELEGRAM_BOT_TOKEN:
    _missing.append("TELEGRAM_BOT_TOKEN")

_raw_webhook_secret = os.getenv("WEBHOOK_SECRET")
WEBHOOK_SECRET = _raw_webhook_secret.strip() if _raw_webhook_secret is not None else ""
if not WEBHOOK_SECRET:
    _missing.append("WEBHOOK_SECRET")

_raw_supabase_url = os.getenv("SUPABASE_URL")
SUPABASE_URL = _raw_supabase_url.strip() if _raw_supabase_url is not None else ""
if not SUPABASE_URL:
    _missing.append("SUPABASE_URL")
else:
    SUPABASE_URL = SUPABASE_URL.rstrip("/")

_raw_supabase_key = os.getenv("SUPABASE_SECRET_KEY")
SUPABASE_SECRET_KEY = _raw_supabase_key.strip() if _raw_supabase_key is not None else ""
if not SUPABASE_SECRET_KEY:
    _missing.append("SUPABASE_SECRET_KEY")

if _missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(_missing)}")

# Read optional currency symbol (defaults to empty string)
_raw_currency_symbol = os.getenv("CURRENCY_SYMBOL")
CURRENCY_SYMBOL = _raw_currency_symbol.strip() if _raw_currency_symbol is not None else ""
