"""Supabase database operations for TradeBook via REST API."""

import logging
from datetime import datetime
import httpx
from config import SUPABASE_URL, SUPABASE_SECRET_KEY, TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)

BASE = f"{SUPABASE_URL}/rest/v1"
HEADERS = {
    "apikey": SUPABASE_SECRET_KEY,
    "Content-Type": "application/json",
}

# Reusable HTTP client with 10.0s timeout
_client = httpx.Client(timeout=10.0)


def insert_entry(
    trader_id: int,
    update_id: int,
    kind: str,
    item: str | None,
    qty: float | None,
    amount: float,
    note: str | None,
    raw_text: str | None,
) -> dict | None:
    """Insert a new trade or expense entry. Returns row or None if duplicate update."""
    payload = {
        "trader_id": trader_id,
        "update_id": update_id,
        "kind": kind,
        "item": item,
        "qty": qty,
        "amount": amount,
        "note": note,
        "raw_text": raw_text,
    }
    params = {"on_conflict": "update_id"}
    headers = {
        **HEADERS,
        "Prefer": "resolution=ignore-duplicates,return=representation",
    }
    response = _client.post(
        f"{BASE}/entries",
        json=payload,
        params=params,
        headers=headers,
    )
    response.raise_for_status()
    data = response.json()
    return data[0] if data else None


def fetch_entries(
    trader_id: int,
    since: datetime | None = None,
    kinds: list[str] | None = None,
) -> list[dict]:
    """Fetch entries for a trader with optional date filter and kinds filter."""
    params: dict[str, str | int] = {
        "select": "id,kind,item,qty,amount,note,created_at",
        "trader_id": f"eq.{trader_id}",
        "order": "id.asc",
    }
    if since is not None:
        params["created_at"] = f"gte.{since.isoformat()}"
    if kinds:
        params["kind"] = f"in.({','.join(kinds)})"

    rows: list[dict] = []
    offset = 0
    limit = 1000
    while True:
        page_params = {**params, "limit": limit, "offset": offset}
        response = _client.get(
            f"{BASE}/entries",
            params=page_params,
            headers=HEADERS,
        )
        response.raise_for_status()
        data = response.json()
        rows.extend(data)
        if len(data) < limit:
            break
        offset += limit
    return rows


def get_last_entry(trader_id: int) -> dict | None:
    """Get the most recent entry for a trader."""
    params = {
        "select": "id,kind,item,qty,amount,note",
        "trader_id": f"eq.{trader_id}",
        "order": "id.desc",
        "limit": 1,
    }
    response = _client.get(
        f"{BASE}/entries",
        params=params,
        headers=HEADERS,
    )
    response.raise_for_status()
    data = response.json()
    return data[0] if data else None


def delete_entry(entry_id: int, trader_id: int) -> None:
    """Delete a specific entry for a trader."""
    params = {
        "id": f"eq.{entry_id}",
        "trader_id": f"eq.{trader_id}",
    }
    headers = {**HEADERS, "Prefer": "return=minimal"}
    response = _client.delete(
        f"{BASE}/entries",
        params=params,
        headers=headers,
    )
    response.raise_for_status()


def save_receipt_photo(
    trader_id: int,
    update_id: int,
    entry_id: int,
    photo_list: list,
) -> bool:
    """Download largest receipt photo from Telegram and upload to Supabase Storage."""
    if not photo_list or not isinstance(photo_list, list):
        return False

    largest = photo_list[-1]
    if not isinstance(largest, dict):
        return False

    file_id = largest.get("file_id")
    file_size = largest.get("file_size")

    if not file_id:
        return False

    # Step 1: Skip photo if over 5,000,000 bytes
    if file_size is not None and file_size > 5_000_000:
        return False

    try:
        # Step 2: Get file path from Telegram
        resp_file = _client.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile",
            params={"file_id": file_id},
        )
        resp_file.raise_for_status()
        file_info = resp_file.json()
        if not file_info.get("ok"):
            return False

        file_path = file_info.get("result", {}).get("file_path")
        if not file_path:
            return False

        # Step 3: Download photo bytes from Telegram
        resp_bytes = _client.get(
            f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        )
        resp_bytes.raise_for_status()
        photo_bytes = resp_bytes.content
        if len(photo_bytes) > 5_000_000:
            return False

        # Step 4: Upload to Supabase Storage
        storage_url = f"{SUPABASE_URL}/storage/v1/object/receipts/{trader_id}/{update_id}.jpg"
        upload_headers = {
            "apikey": SUPABASE_SECRET_KEY,
            "Content-Type": "image/jpeg",
        }
        resp_upload = _client.post(
            storage_url,
            content=photo_bytes,
            headers=upload_headers,
        )
        resp_upload.raise_for_status()

        # Step 5: Patch entries table with receipt_path
        receipt_path = f"{trader_id}/{update_id}.jpg"
        resp_patch = _client.patch(
            f"{BASE}/entries",
            params={"id": f"eq.{entry_id}"},
            json={"receipt_path": receipt_path},
            headers=HEADERS,
        )
        resp_patch.raise_for_status()
        return True

    except httpx.HTTPStatusError as exc:
        logger.error("Receipt photo HTTP error: status=%s", exc.response.status_code)
        return False
    except Exception:
        logger.error("Receipt photo processing error")
        return False

