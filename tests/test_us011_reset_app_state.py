"""US-011 - Reset App State.

As a customer, I want to reset the application state, so that I can clear my
shopping session.
"""
import pytest

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


@pytest.mark.session
def test_reset_app_state_clears_cart(inventory_page):
    """Resetting the app state empties the cart badge."""
    # Given the user has products in the cart
    for product in PRODUCTS:
        inventory_page.add_product_to_cart(product)
    assert inventory_page.get_cart_badge_count() == len(PRODUCTS)

    # When the user opens the side menu and clicks "Reset App State"
    inventory_page.menu.reset_app_state()

    # Then the cart badge disappears
    assert not inventory_page.is_cart_badge_visible()
    assert inventory_page.get_cart_badge_count() == 0
