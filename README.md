# TradeBook

TradeBook is a lightweight Telegram bot designed for small shopkeepers and market traders to record daily transactions through plain text messages. It logs sales, stock purchases, and expenses to track real-time inventory and provide rolling 7-day cash flow summaries without requiring complicated accounting software.

---

## The Problem

Most small shopkeepers and market traders record their business on paper notebooks or try to keep numbers in their head. Paper notebooks get misplaced, torn, water-damaged, or forgotten at home, while dedicated accounting apps are too complicated, consume too much data, and require steep learning curves. As a result, traders struggle to answer basic daily questions: *How much stock do I actually have left? How much cash came in this week? Am I making a profit?* Without clear records, they also cannot prove their business turnover when applying for small business loans or microcredit.

---

## How to Use It

Traders talk to TradeBook by typing plain text messages directly in Telegram.

### Commands & Examples

- **Record a sale**:
  ```text
  sold 3 rice 15000
  ```
  *(Format: quantity, item, total money received)*
  - Bot reply: `Recorded sale: 3 rice = 15,000`

- **Record stock bought**:
  ```text
  bought 10 rice 60000
  ```
  *(Format: quantity, item, total money paid)*
  - Bot reply: `Recorded purchase: 10 rice = 60,000`

- **Record an expense**:
  ```text
  expense 2000 transport
  ```
  *(Format: amount, description of expense)*
  - Bot reply: `Recorded expense: 2,000 - transport`

- **Check current stock**:
  ```text
  stock
  ```
  - Bot reply:
    ```text
    Stock (bought minus sold):
    - beans: 15
    - palm oil: 8
    - rice: 7
    ```
  *(If sales exceed purchases, it shows: `- rice: -2 (you sold more than you logged as bought)`)*

- **Weekly summary**:
  ```text
  summary
  ```
  - Bot reply:
    ```text
    Last 7 days
    Money in (sales): 45,000
    Money out (stock bought): 60,000
    Expenses: 2,000
    Net: -17,000
    Top sellers: rice 30,000; beans 15,000
    Entries: 8
    ```

- **Undo last entry**:
  ```text
  undo
  ```
  - Bot reply: `Removed sale: 3 rice = 15,000` *(or `Nothing to undo.` if empty)*

- **Help / Instructions**:
  ```text
  help
  ```
  *(or `/start`)* displays the quick command guide.

- **Receipt photos**:
  Send any receipt photo with a caption like `sold 3 rice 15000`. TradeBook records the entry and saves the photo directly to Supabase Storage:
  - Bot reply: `Recorded sale: 3 rice = 15,000 (receipt saved)`
  - If a photo is sent without a caption, the bot prompts: `Add a caption like: sold 3 rice 15000`.

---

## Architecture

```text
+--------------------+            HTTPS Webhook             +-----------------------+
|                    |  ==================================> |                       |
|   Trader / User    |                                      | Render Web Service    |
|   (Telegram App)   |  <================================== | (FastAPI sync app)    |
|                    |             Telegram API             |                       |
+--------------------+                                      +-----------------------+
                                                                        |
                                                                        | HTTPS REST API (PostgREST)
                                                                        | apikey header (RLS enabled)
                                                                        v
                                                            +-----------------------+
                                                            |                       |
                                                            |  Supabase PostgreSQL  |
                                                            |  & Storage (receipts) |
                                                            |                       |
                                                            +-----------------------+
```

---

## Tech Stack

- **Language**: Python 3.12 (standardized via `.python-version`)
- **Web Framework**: FastAPI + Uvicorn (synchronous `def` endpoints)
- **HTTP Client**: `httpx` (sync client for Telegram Bot API & Supabase REST API)
- **Database & Storage**: Supabase Postgres via REST API (`/rest/v1`) with Row Level Security (RLS) and Supabase Storage (`/storage/v1`)
- **Environment Management**: `python-dotenv`
- **Hosting**: Render Free Web Service

---

## Run Locally

### 1. Prerequisites
- Python 3.10 to 3.14 (3.12 recommended)
- Git

### 2. Clone and Setup Environment
```bash
git clone https://github.com/SammyCodes1/TradeBook.git
cd TradeBook

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt   # On Windows
# or: source .venv/bin/activate && pip install -r requirements.txt (macOS/Linux)
```

### 3. Configure Database
1. Open your Supabase Project dashboard.
2. Go to the **SQL Editor**, paste the contents of `schema.sql`, and click **Run**.
3. Create a bucket named `receipts` in **Supabase Storage** (under Storage -> New Bucket).

### 4. Setup `.env`
Create a `.env` file based on `.env.example`:
```dotenv
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_from_botfather
WEBHOOK_SECRET=your_random_secret_token
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SECRET_KEY=your_supabase_secret_key
CURRENCY_SYMBOL=
PUBLIC_URL=https://your-domain.ngrok-free.app
```

### 5. Verify Database Connectivity & Run Tests
```bash
# Verify database connection (inserts, reads, and deletes a test entry)
.venv\Scripts\python.exe check_db.py

# Run parser test suite
.venv\Scripts\python.exe test_parser.py
```

### 6. Start Local Webhook Server
```bash
.venv\Scripts\uvicorn.exe main:app --port 8000
```

---

## Deploy on Render

1. Create a new **Web Service** on [Render](https://render.com) connected to your GitHub repository.
2. Configure settings:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add Environment Variables in Render Dashboard:
   - `TELEGRAM_BOT_TOKEN`: Token from BotFather.
   - `WEBHOOK_SECRET`: Secure random string.
   - `SUPABASE_URL`: Supabase project URL (no trailing slash).
   - `SUPABASE_SECRET_KEY`: Supabase secret API key.
   - `CURRENCY_SYMBOL`: *(Optional)* e.g., `₦`, `$`, `£`.
4. Deploy the service and copy your public Render service URL (e.g. `https://tradebook-xxxx.onrender.com`).
5. Register the webhook with Telegram:
   ```bash
   # Set PUBLIC_URL in your local .env or pass it via terminal, then run:
   .venv\Scripts\python.exe set_webhook.py
   ```

---

## Environment Variables

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Bot API token provided by Telegram's @BotFather. |
| `WEBHOOK_SECRET` | Secret token sent by Telegram in `X-Telegram-Bot-Api-Secret-Token` to verify webhook authenticity. |
| `SUPABASE_URL` | Base HTTPS URL of your Supabase project (no trailing slash). |
| `SUPABASE_SECRET_KEY` | Private Supabase secret API key for PostgREST and Storage calls (sent only in `apikey` header). |
| `CURRENCY_SYMBOL` | *(Optional)* Symbol prefixed to money outputs (e.g., `₦`, `$`). Defaults to empty string. |
| `PUBLIC_URL` | *(Used only by `set_webhook.py`)* The public HTTPS URL of your deployed service (no trailing slash). |

---

## Python Version

Specified in `.python-version` as `3.12`. Render and other deployment platforms automatically read this file to guarantee that the cloud deployment executes on the exact same Python interpreter version as the local development environment.

---

## Known Limitations

- **Render Free Tier Spin-Down**: On Render's free tier, the web service automatically sleeps after ~15 minutes of inactivity. When a trader sends a message after an idle period, the first response may take 50–60 seconds while the server spins up. Subsequent messages respond instantly.
- **Supabase Free Project Pausing**: Free-tier Supabase projects pause after 7 consecutive days of inactivity. If paused, the project must be resumed manually from the Supabase web dashboard.
- **Rolling 7-Day Cash Summary**: The weekly summary is a simple rolling 7-day cash view calculated in UTC. It does not perform formal accrual accounting, depreciation, or tax calculations.
- **Telegram Only**: Currently operates solely via Telegram. Traders without Telegram or smartphones cannot yet use the service via SMS or WhatsApp.

---

## Roadmap

- **WhatsApp Integration**: Support WhatsApp Business API so shopkeepers can log sales inside the messaging app they already use daily.
- **Receipt OCR & Auto-Extraction**: Automatically read totals and items from uploaded receipt pictures using lightweight optical character recognition.
- **Local-Language & Voice Support**: Accept voice notes and input in local languages/dialects (e.g., Nigerian Pidgin, Hausa, Yoruba, Swahili).
- **Lender-Ready Monthly Reports**: Generate structured monthly PDF cash flow summaries that traders can present to micro-finance banks and lenders to access working capital loans.
