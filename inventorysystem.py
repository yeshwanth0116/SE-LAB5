"""Simple inventory system used for static-analysis lab exercises.

This module intentionally contains issues in the starter version; the
fixed version documents and addresses common problems (mutable defaults,
bare except, use of eval, missing context managers, etc.).
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)

# Global variable (kept for simplicity in this lab)
stock_data: Dict[str, int] = {}


def add_item(
    item: str = "default",
    qty: int = 0,
    logs: Optional[List[str]] = None,
) -> None:
    """Add quantity to an item in stock.

    Args:
        item: item name (must be a string).
        qty: integer quantity to add (can be negative to remove).
        logs: optional list to append log entries to.
    """
    if logs is None:
        logs = []
    if not item or not isinstance(item, str):
        logging.warning("add_item called with invalid item: %r", item)
        return
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        logging.warning("add_item called with non-integer qty: %r", qty)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item: str, qty: int) -> None:
    """Remove quantity from an item; uses explicit KeyError handling."""
    if not isinstance(item, str):
        logging.warning("remove_item called with invalid item: %r", item)
        return
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        logging.warning("remove_item called with non-integer qty: %r", qty)
        return

    if item not in stock_data:
        logging.info("remove_item: %s not found in stock", item)
        return

    stock_data[item] -= qty
    if stock_data[item] <= 0:
        del stock_data[item]


def get_qty(item: str) -> int:
    """Return quantity for an item, or 0 if missing."""
    if not isinstance(item, str):
        raise TypeError("item name must be a string")
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load stock data from a JSON file using a context manager."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        logging.info("load_data: %s not found", file)
        logging.info("starting with empty stock")
        stock_data = {}
    except json.JSONDecodeError as e:
        logging.error("load_data: invalid JSON in %s: %s", file, e)
        stock_data = {}


def save_data(file: str = "inventory.json") -> None:
    """Save stock data to a JSON file using a context manager."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f)


def print_data() -> None:
    """Print a simple items report to stdout."""
    print("Items Report")
    for i, qty in stock_data.items():
        print(i, "->", qty)


def check_low_items(threshold: int = 5) -> List[str]:
    """Return list of items with quantity below threshold."""
    try:
        threshold = int(threshold)
    except (TypeError, ValueError):
        logging.warning("check_low_items: invalid threshold %r", threshold)
        threshold = 5

    return [i for i, q in stock_data.items() if q < threshold]


def main() -> None:
    """Example usage of the inventory helpers."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item("pear", 3)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    logging.info("Finished main run")


if __name__ == "__main__":
    main()
