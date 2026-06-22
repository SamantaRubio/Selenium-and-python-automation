"""US-006 - Remove Product From Cart.

As a customer, I want to remove products from the cart, so that I can modify
my purchase.
"""
import pytest

PRODUCT = "Sauce Labs Backpack"


@pytest.mark.cart
def test_remove_product_from_inventory_updates_badge(inventory_page):
    """Removing a product from the inventory page clears the cart badge."""
    # Given a product is already in the cart
    inventory_page.add_product_to_cart(PRODUCT)
    assert inventory_page.get_cart_badge_count() == 1

    # When the user clicks "Remove"
    inventory_page.remove_product_from_cart(PRODUCT)

    # Then the cart badge updates accordingly (back to empty)
    assert inventory_page.get_cart_badge_count() == 0
    # And the button returns to "Add to cart"
    assert inventory_page.get_product_button_text(PRODUCT).lower() == "add to cart"


@pytest.mark.cart
def test_remove_product_from_cart_page(inventory_page):
    """Removing a product from within the cart page empties the cart."""
    inventory_page.add_product_to_cart(PRODUCT)
    cart = inventory_page.go_to_cart()
    assert cart.contains_product(PRODUCT)

    # When the user clicks "Remove" on the cart page
    cart.click(cart.REMOVE_BUTTON)

    # Then the product disappears from the cart and the badge is gone.
    assert cart.get_item_count() == 0
    assert cart.get_cart_badge_count() == 0
