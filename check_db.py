"""Database verification script for TradeBook."""

import sys
import time
import httpx
from db import insert_entry, fetch_entries, delete_entry


def main():
    test_update_id = -int(time.time())
    try:
        # 1. Insert test row
        row = insert_entry(
            trader_id=0,
            update_id=test_update_id,
            kind="sale",
            item="test",
            qty=1,
            amount=1,
            note=None,
            raw_text="check_db test",
        )
        if not row or "id" not in row:
            print("DB check failed: insert_entry did not return an inserted row with an id")
            sys.exit(1)

        entry_id = row["id"]

        # 2. Confirm it can be read back with fetch_entries(0)
        entries = fetch_entries(trader_id=0)
        found = any(e.get("id") == entry_id for e in entries)
        if not found:
            print(f"DB check failed: could not read back inserted row id {entry_id}")
            sys.exit(1)

        # 3. Delete it with delete_entry
        delete_entry(entry_id=entry_id, trader_id=0)

        # 4. Confirm it is gone
        entries_after = fetch_entries(trader_id=0)
        still_exists = any(e.get("id") == entry_id for e in entries_after)
        if still_exists:
            print(f"DB check failed: row id {entry_id} was not deleted")
            sys.exit(1)

        print("DB CHECK PASSED")

    except httpx.HTTPStatusError as exc:
        print(f"DB check failed: HTTP {exc.response.status_code} - {exc.response.text}")
        sys.exit(1)
    except Exception as exc:
        print(f"DB check failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
