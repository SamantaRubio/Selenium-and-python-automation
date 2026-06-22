"""US-003 - View Products.

As a customer, I want to view the products list, so that I can browse
available items.
"""
import pytest


@pytest.mark.products
def test_products_list_is_displayed(inventory_page):
    """The inventory page lists the available products."""
    assert inventory_page.is_loaded()
    assert inventory_page.get_product_count() == 6, "SauceDemo lists 6 products"


@pytest.mark.products
def test_each_product_shows_required_details(inventory_page):
    """Every product card exposes image, name, description, price and button."""
    # Spot-check the first card explicitly for clearer failure messages...
    details = inventory_page.get_first_product_details()
    assert details["has_image"], "Product should display an image"
    assert details["name"], "Product should display a name"
    assert details["description"], "Product should display a description"
    assert details["price"].startswith("$"), "Product should display a price"
    assert details["button_text"], "Product should display an action button"

    # ...then assert the same completeness across all cards.
    assert inventory_page.each_product_is_complete()
