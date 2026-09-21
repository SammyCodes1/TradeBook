"""TradeBook message handlers and business logic."""

from datetime import datetime, timedelta, timezone
from config import CURRENCY_SYMBOL
import db
import parsing


def fmt_num(x: float | int) -> str:
    """Format a number: round to 2 decimals, thousands separators, no trailing zeros."""
    val = round(float(x), 2)
    if val.is_integer():
        return f"{int(val):,}"
    return f"{val:,.2f}".rstrip("0").rstrip(".")


def money(x: float | int) -> str:
    """Format money with CURRENCY_SYMBOL, keeping a leading negative sign if negative."""
    val = round(float(x), 2)
    if val < 0 and CURRENCY_SYMBOL:
        return f"-{CURRENCY_SYMBOL}{fmt_num(abs(val))}"
    return f"{CURRENCY_SYMBOL}{fmt_num(val)}"


def describe(entry: dict) -> str:
    """Describe an entry row in plain text."""
    kind = entry.get("kind")
    amount = float(entry.get("amount") or 0)
    if kind == "expense":
        note = entry.get("note") or ""
        return f"expense: {money(amount)} - {note}"
    qty = float(entry.get("qty") or 0)
    item = entry.get("item") or ""
    return f"{kind}: {fmt_num(qty)} {item} = {money(amount)}"


def handle_text(
    trader_id: int,
    update_id: int,
    text: str,
    photo_list: list | None = None,
) -> str | None:
    """Process incoming text message from a trader and return the reply text."""
    parsed = parsing.parse_message(text)

    if parsed.cmd == "help":
        return parsing.HELP_TEXT

    if parsed.cmd == "unknown":
        return "I didn't understand that. Send 'help' to see what I can do."

    if parsed.cmd == "error":
        return parsed.error

    if parsed.cmd == "entry":
        row = db.insert_entry(
            trader_id=trader_id,
            update_id=update_id,
            kind=parsed.kind,
            item=parsed.item,
            qty=parsed.qty,
            amount=parsed.amount,
            note=parsed.note,
            raw_text=text,
        )
        if row is None:
            return None
        reply = "Recorded " + describe(row)
        if photo_list:
            if db.save_receipt_photo(trader_id, update_id, row["id"], photo_list):
                reply += " (receipt saved)"
            else:
                reply += " (photo not saved)"
        return reply

    if parsed.cmd == "undo":
        entry = db.get_last_entry(trader_id)
        if entry is None:
            return "Nothing to undo."
        db.delete_entry(entry["id"], trader_id)
        return "Removed " + describe(entry)

    if parsed.cmd == "stock":
        rows = db.fetch_entries(trader_id, kinds=["sale", "purchase"])
        if not rows:
            return "No stock recorded yet. Log stock with: bought 10 rice 60000"

        stock_counts: dict[str, float] = {}
        for r in rows:
            item = r.get("item")
            if not item:
                continue
            qty = float(r.get("qty") or 0)
            if r.get("kind") == "purchase":
                stock_counts[item] = stock_counts.get(item, 0.0) + qty
            elif r.get("kind") == "sale":
                stock_counts[item] = stock_counts.get(item, 0.0) - qty

        lines = ["Stock (bought minus sold):"]
        for item in sorted(stock_counts.keys()):
            qty = stock_counts[item]
            if qty < 0:
                lines.append(
                    f"- {item}: {fmt_num(qty)} (you sold more than you logged as bought)"
                )
            else:
                lines.append(f"- {item}: {fmt_num(qty)}")
        return "\n".join(lines)

    if parsed.cmd == "summary":
        since = datetime.now(timezone.utc) - timedelta(days=7)
        rows = db.fetch_entries(trader_id, since=since)
        if not rows:
            return "No entries in the last 7 days."

        sales_total = 0.0
        purchases_total = 0.0
        expenses_total = 0.0
        sales_by_item: dict[str, float] = {}

        for r in rows:
            kind = r.get("kind")
            amt = float(r.get("amount") or 0)
            if kind == "sale":
                sales_total += amt
                item = r.get("item")
                if item:
                    sales_by_item[item] = sales_by_item.get(item, 0.0) + amt
            elif kind == "purchase":
                purchases_total += amt
            elif kind == "expense":
                expenses_total += amt

        net = sales_total - purchases_total - expenses_total

        lines = [
            "Last 7 days",
            f"Money in (sales): {money(sales_total)}",
            f"Money out (stock bought): {money(purchases_total)}",
            f"Expenses: {money(expenses_total)}",
            f"Net: {money(net)}",
        ]

        if sales_by_item:
            top_items = sorted(
                sales_by_item.items(), key=lambda x: (-x[1], x[0])
            )[:3]
            top_str = "; ".join(f"{item} {money(amt)}" for item, amt in top_items)
            lines.append(f"Top sellers: {top_str}")

        lines.append(f"Entries: {len(rows)}")
        return "\n".join(lines)

    return "I didn't understand that. Send 'help' to see what I can do."
