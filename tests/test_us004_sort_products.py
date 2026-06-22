"""US-004 - Sort Products.

As a customer, I want to sort products, so that I can organize items
according to my preference.
"""
import pytest

from pages.inventory_page import InventoryPage


@pytest.mark.products
def test_sort_name_a_to_z(inventory_page):
    """Sorting by 'Name (A to Z)' orders products alphabetically ascending."""
    inventory_page.sort_products(InventoryPage.SORT_NAME_AZ)
    names = inventory_page.get_product_names()
    assert names == sorted(names)


@pytest.mark.products
def test_sort_name_z_to_a(inventory_page):
    """Sorting by 'Name (Z to A)' orders products alphabetically descending."""
    inventory_page.sort_products(InventoryPage.SORT_NAME_ZA)
    names = inventory_page.get_product_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.products
def test_sort_price_low_to_high(inventory_page):
    """Sorting by 'Price (low to high)' orders products by ascending price."""
    inventory_page.sort_products(InventoryPage.SORT_PRICE_LOW_HIGH)
    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices)


@pytest.mark.products
def test_sort_price_high_to_low(inventory_page):
    """Sorting by 'Price (high to low)' orders products by descending price."""
    inventory_page.sort_products(InventoryPage.SORT_PRICE_HIGH_LOW)
    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices, reverse=True)
