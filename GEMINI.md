# TradeBook: rules for this project

## Product
TradeBook is a Telegram bot for small traders and shop owners. They type short messages
like "sold 3 rice 15000". The bot records them, tracks stock, and gives a weekly summary.
This is a hackathon MVP. Small, correct and readable beats clever.

## Fixed stack (do not add, swap or upgrade anything)
- Python 3.10 to 3.14, matching the interpreter on this machine (the repo's `.python-version` file makes Render use the same version)
- FastAPI + uvicorn. Use SYNC endpoints (`def`, not `async def`).
- httpx (sync `httpx.Client`) for ALL outside calls: Telegram Bot API and Supabase REST API.
- python-dotenv for loading a local .env file.
- Supabase Postgres accessed ONLY through its REST API (`{SUPABASE_URL}/rest/v1/...`) using httpx.
  No supabase-py, no SQLAlchemy, no ORM.
- Hosting: Render free web service. Telegram WEBHOOK mode only. NEVER use polling.
- Allowed dependencies in requirements.txt: fastapi, uvicorn, httpx, python-dotenv. Nothing else.

## Hard rules
1. Do not add features, files, endpoints, classes or abstractions the current prompt did not ask for.
2. Do not guess. If you need a fact that is missing (a key name, URL, behaviour), stop and ask me.
3. Secrets: never hard-code them, never print them. Never log request URLs (the Telegram token is inside the URL).
   Never log message text. Never create or edit a real `.env` with real values; only `.env.example`.
4. Never run `git push`, never deploy, and never call the real Telegram or Supabase APIs unless the prompt says so.
5. Send the Supabase key ONLY in the `apikey` header. Do NOT send `Authorization: Bearer`
   (new Supabase secret keys are not JWTs and are rejected in that header).
6. Telegram replies are plain text. Do NOT use parse_mode.
7. /webhook must return HTTP 200 for every request that passes the secret check, even if our code fails
   (non-2xx makes Telegram retry). Log the error and return {"ok": true}.
8. Work only on the current prompt. When finished, print: files created/changed, commands run, test results. Then stop and wait.
9. Short plain-English comments. Clear names. Small functions.
10. Code must run on Windows, macOS and Linux (use pathlib; no shell-specific code inside the app).
11. Pass all HTTP query filters through httpx `params=`, never by string concatenation.

## Data meaning (never change)
- `sold 3 rice 15000` = 3 units of rice sold; 15000 is the TOTAL money received (not per unit).
- `bought 10 rice 60000` = 10 units added to stock; 60000 is the TOTAL money paid.
- `expense 2000 transport` = money spent on something else.
- Stock per item = total bought qty minus total sold qty.
- Summary = rolling last 7 days (UTC). Money in = sales. Money out = purchases + expenses. Net = in minus out.
  This is a simple cash view, not formal accounting.
- A trader = a Telegram user id. A trader only ever sees their own rows.

## Final file layout
main.py, handlers.py, parsing.py, db.py, telegram_api.py, config.py, set_webhook.py, check_db.py,
schema.sql, test_parser.py, requirements.txt, .python-version, .env.example, .gitignore, README.md, GEMINI.md
(Optional later: SUBMISSION.md)
