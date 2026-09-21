"""Supabase database operations for TradeBook via REST API."""

from datetime import datetime
import httpx
from config import SUPABASE_URL, SUPABASE_SECRET_KEY

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
