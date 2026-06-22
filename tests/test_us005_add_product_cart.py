"""US-005 - Add Product To Cart.

As a customer, I want to add products to the shopping cart, so that I can
purchase them later.
"""
import pytest

PRODUCT = "Sauce Labs Backpack"


@pytest.mark.cart
def test_add_product_increases_badge_and_toggles_button(inventory_page):
    """Adding a product updates the cart badge and the button label."""
    # Given the cart starts empty
    assert inventory_page.get_cart_badge_count() == 0

    # When the user adds a product to the cart
    inventory_page.add_product_to_cart(PRODUCT)

    # Then the cart badge increases by 1
    assert inventory_page.get_cart_badge_count() == 1
    # And the button changes to "Remove"
    assert inventory_page.get_product_button_text(PRODUCT).lower() == "remove"


@pytest.mark.cart
def test_add_multiple_products_updates_badge(inventory_page):
    """Adding several products keeps the badge count accurate."""
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")
    assert inventory_page.get_cart_badge_count() == 2
