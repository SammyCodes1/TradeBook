"""TradeBook message parser."""

from dataclasses import dataclass
import re

HELP_TEXT = """TradeBook - your shop's notebook

Log a sale: sold 3 rice 15000
(quantity, item, TOTAL money received)

Log stock you bought: bought 10 rice 60000
(quantity, item, TOTAL money you paid)

Log an expense: expense 2000 transport

Check stock: stock
Last 7 days report: summary
Undo your last entry: undo"""

_CURRENCY_CHARS = {",", "₦", "$", "£", "€"}
_NUM_RE = re.compile(r"^\d+(\.\d+)?$")

_ERROR_SOLD = "I couldn't read that. Use: sold 3 rice 15000 (quantity, item, total money received)"
_ERROR_BOUGHT = "I couldn't read that. Use: bought 10 rice 60000 (quantity, item, total money paid)"
_ERROR_EXPENSE = "I couldn't read that. Use: expense 2000 transport (amount, what for)"


@dataclass
class Parsed:
    cmd: str
    kind: str | None = None
    item: str | None = None
    qty: float | None = None
    amount: float | None = None
    note: str | None = None
    error: str | None = None


def _parse_number(token: str) -> float | None:
    # Strip commas and currency symbols
    cleaned = "".join(ch for ch in token if ch not in _CURRENCY_CHARS)
    if not _NUM_RE.match(cleaned):
        return None
    try:
        val = float(cleaned)
    except ValueError:
        return None
    if val <= 0 or val >= 1e12:
        return None
    return val


def parse_message(text: str) -> Parsed:
    tokens = text.strip().split()
    if not tokens:
        return Parsed(cmd="unknown")

    # Command word: lowercased, remove leading / and @botname suffix
    raw_cmd = tokens[0].lower()
    if raw_cmd.startswith("/"):
        raw_cmd = raw_cmd[1:]
    raw_cmd = raw_cmd.split("@")[0]

    if raw_cmd in ("start", "help"):
        return Parsed(cmd="help")

    if raw_cmd in ("stock", "summary", "undo"):
        return Parsed(cmd=raw_cmd)

    if raw_cmd in ("sold", "bought"):
        err_msg = _ERROR_SOLD if raw_cmd == "sold" else _ERROR_BOUGHT
        kind = "sale" if raw_cmd == "sold" else "purchase"

        # Needs at least 3 tokens after command: qty, item..., amount
        if len(tokens) < 4:
            return Parsed(cmd="error", error=err_msg)

        qty = _parse_number(tokens[1])
        amount = _parse_number(tokens[-1])
        item_words = tokens[2:-1]
        item = " ".join(item_words).lower()

        # Item must contain at least one letter and not exceed 60 characters
        has_letter = any(ch.isalpha() for ch in item)
        if qty is None or amount is None or not has_letter or len(item) > 60:
            return Parsed(cmd="error", error=err_msg)

        return Parsed(cmd="entry", kind=kind, item=item, qty=qty, amount=amount)

    if raw_cmd == "expense":
        # Needs amount and at least one note word
        if len(tokens) < 3:
            return Parsed(cmd="error", error=_ERROR_EXPENSE)

        amount = _parse_number(tokens[1])
        note = " ".join(tokens[2:])

        if amount is None or not note:
            return Parsed(cmd="error", error=_ERROR_EXPENSE)

        return Parsed(cmd="entry", kind="expense", amount=amount, note=note)

    return Parsed(cmd="unknown")
