"""US-007 - View Cart.

As a customer, I want to review my cart, so that I can verify selected items.
"""
import pytest

from pages.cart_page import CartPage

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


@pytest.mark.cart
def test_cart_displays_selected_products(inventory_page):
    """Opening the cart shows every product the user added."""
    # Given the user has products in the cart
    for product in PRODUCTS:
        inventory_page.add_product_to_cart(product)

    # When the user clicks the cart icon
    cart = inventory_page.go_to_cart()

    # Then the cart page opens
    assert cart.is_loaded()
    assert CartPage.URL_FRAGMENT in cart.get_current_url()

    # And all selected products are displayed
    assert cart.get_item_count() == len(PRODUCTS)
    for product in PRODUCTS:
        assert cart.contains_product(product), f"{product} should appear in the cart"
