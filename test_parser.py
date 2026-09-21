"""Tests for parsing.py."""

from parsing import parse_message


def run_tests():
    # Case 1: "sold 3 rice 15000" -> entry, sale, item "rice", qty 3, amount 15000
    p1 = parse_message("sold 3 rice 15000")
    assert p1.cmd == "entry"
    assert p1.kind == "sale"
    assert p1.item == "rice"
    assert p1.qty == 3
    assert p1.amount == 15000

    # Case 2: "  SOLD   3   Rice   15,000 " -> same as 1
    p2 = parse_message("  SOLD   3   Rice   15,000 ")
    assert p2.cmd == "entry"
    assert p2.kind == "sale"
    assert p2.item == "rice"
    assert p2.qty == 3
    assert p2.amount == 15000

    # Case 3: "/sold 3 rice ₦15,000" -> same as 1
    p3 = parse_message("/sold 3 rice ₦15,000")
    assert p3.cmd == "entry"
    assert p3.kind == "sale"
    assert p3.item == "rice"
    assert p3.qty == 3
    assert p3.amount == 15000

    # Case 4: "sold 2 palm oil 12500" -> item "palm oil", qty 2, amount 12500
    p4 = parse_message("sold 2 palm oil 12500")
    assert p4.cmd == "entry"
    assert p4.kind == "sale"
    assert p4.item == "palm oil"
    assert p4.qty == 2
    assert p4.amount == 12500

    # Case 5: "sold 1.5 beans 4000" -> qty 1.5
    p5 = parse_message("sold 1.5 beans 4000")
    assert p5.cmd == "entry"
    assert p5.kind == "sale"
    assert p5.item == "beans"
    assert p5.qty == 1.5
    assert p5.amount == 4000

    # Case 6: "bought 10 rice 60000" -> entry, purchase, qty 10, item "rice", amount 60000
    p6 = parse_message("bought 10 rice 60000")
    assert p6.cmd == "entry"
    assert p6.kind == "purchase"
    assert p6.qty == 10
    assert p6.item == "rice"
    assert p6.amount == 60000

    # Case 7: "expense 2000 bus fare" -> entry, expense, amount 2000, note "bus fare", item None, qty None
    p7 = parse_message("expense 2000 bus fare")
    assert p7.cmd == "entry"
    assert p7.kind == "expense"
    assert p7.amount == 2000
    assert p7.note == "bus fare"
    assert p7.item is None
    assert p7.qty is None

    # Case 8: "/stock", "stock", "/stock@TradeBookBot", "STOCK please" -> cmd "stock"
    for text in ["/stock", "stock", "/stock@TradeBookBot", "STOCK please"]:
        p8 = parse_message(text)
        assert p8.cmd == "stock", f"Failed for {text!r}: {p8}"

    # Case 9: "summary" -> "summary"; "undo" -> "undo"; "help" -> "help"; "/start" -> "help"
    assert parse_message("summary").cmd == "summary"
    assert parse_message("undo").cmd == "undo"
    assert parse_message("help").cmd == "help"
    assert parse_message("/start").cmd == "help"

    # Case 10: These must return cmd "error" with a non-empty error:
    # "sold rice 3 15000", "sold 3 rice", "sold 0 rice 100", "sold 3 rice -100", "sold 3 15000 5000",
    # "bought 10 rice", "expense 2000", "expense transport 2000", "sold 3 rice abc"
    error_cases = [
        "sold rice 3 15000",
        "sold 3 rice",
        "sold 0 rice 100",
        "sold 3 rice -100",
        "sold 3 15000 5000",
        "bought 10 rice",
        "expense 2000",
        "expense transport 2000",
        "sold 3 rice abc",
    ]
    for text in error_cases:
        pe = parse_message(text)
        assert pe.cmd == "error", f"Expected 'error' for {text!r}, got {pe.cmd}"
        assert pe.error and len(pe.error) > 0, f"Expected non-empty error for {text!r}"

    # Case 11: These must return cmd "unknown": "hello", "", "   ", "12345"
    for text in ["hello", "", "   ", "12345"]:
        pu = parse_message(text)
        assert pu.cmd == "unknown", f"Expected 'unknown' for {text!r}, got {pu.cmd}"

    print("All parser tests passed")


if __name__ == "__main__":
    run_tests()
