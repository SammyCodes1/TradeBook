# TradeBook

TradeBook is a Telegram bot for small traders and shop owners. It records simple text messages like `"sold 3 rice 15000"`, tracks stock inventory, and provides weekly summaries.

## Features
- **Fast logging**: Record sales (`sold 3 rice 15000`), purchases (`bought 10 rice 60000`), and expenses (`expense 2000 transport`).
- **Inventory tracking**: Check current stock with `stock` (total bought minus total sold).
- **Weekly summaries**: Rolling 7-day cash flow summary (Money in, Money out, Expenses, Net, and Top Sellers) with `summary`.
- **Undo**: Remove the last entry with `undo`.
- **Deduplication**: Enforced idempotent processing via Telegram's `update_id`.
- **Data isolation**: Traders only ever see their own records.

## Tech Stack
- **Runtime**: Python 3.12+
- **API Framework**: FastAPI + Uvicorn (sync endpoints)
- **Database**: Supabase Postgres via REST API (`httpx`)
- **Integration**: Telegram Bot Webhook API

## Project Layout
```
├── config.py          # Environment variables and configuration
├── db.py              # Supabase REST API operations
├── handlers.py        # Message handling and business logic
├── main.py            # FastAPI webhook application
├── parsing.py         # Text parsing and command extraction
├── telegram_api.py    # Telegram Bot API client
├── check_db.py        # Database connectivity test script
├── set_webhook.py     # Webhook setup script for Telegram
├── test_parser.py     # Parser test suite
├── schema.sql         # Supabase PostgreSQL schema
├── requirements.txt   # Dependencies (fastapi, uvicorn, httpx, python-dotenv)
├── .env.example       # Example environment variables template
└── .python-version    # Target Python version for deployment
```

## Setup Instructions

### 1. Install Dependencies
```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt  # On Windows
# or: source .venv/bin/activate && pip install -r requirements.txt (macOS/Linux)
```

### 2. Configure Database
Paste and run `schema.sql` inside the Supabase SQL Editor to create the `entries` table and index.

### 3. Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
WEBHOOK_SECRET=your_webhook_secret
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SECRET_KEY=your_supabase_secret_key
CURRENCY_SYMBOL=
PUBLIC_URL=https://your-service.onrender.com
```

### 4. Verify Database
```bash
python check_db.py
```

### 5. Start Server
```bash
uvicorn main:app --port 8000
```

### 6. Set Webhook
```bash
python set_webhook.py
```

## Testing
Run the parser test suite:
```bash
python test_parser.py
```
