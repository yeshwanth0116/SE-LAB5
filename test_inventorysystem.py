import json
import os
import inventorysystem as inv


def setup_function():
    # ensure a clean global state before each test
    inv.stock_data.clear()


def test_add_and_get_qty():
    inv.add_item("apple", 5)
    assert inv.get_qty("apple") == 5
    inv.add_item("apple", 3)
    assert inv.get_qty("apple") == 8


def test_remove_item():
    inv.add_item("banana", 4)
    inv.remove_item("banana", 2)
    assert inv.get_qty("banana") == 2
    inv.remove_item("banana", 2)
    assert inv.get_qty("banana") == 0


def test_load_save(tmp_path):
    inv.add_item("pear", 7)
    p = tmp_path / "test_inv.json"
    inv.save_data(str(p))
    # clear and reload
    inv.stock_data.clear()
    inv.load_data(str(p))
    assert inv.get_qty("pear") == 7


def test_invalid_inputs():
    # empty item name is ignored
    inv.add_item("", 5)
    assert inv.get_qty("") == 0

    # non-integer qty is ignored
    inv.add_item("grape", "notint")
    assert inv.get_qty("grape") == 0
