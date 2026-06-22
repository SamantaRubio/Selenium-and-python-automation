"""US-009 - Cancel Checkout.

As a customer, I want to cancel the checkout process, so that I can return to
shopping.
"""
import pytest

from config.config import CheckoutData
from pages.inventory_page import InventoryPage

PRODUCT = "Sauce Labs Backpack"


@pytest.mark.checkout
def test_cancel_checkout_returns_to_inventory(inventory_page):
    """Cancelling the checkout returns the user to the inventory page."""
    # Given the user is in the checkout flow (overview step)
    inventory_page.add_product_to_cart(PRODUCT)
    checkout = inventory_page.go_to_cart().proceed_to_checkout()
    checkout.fill_information(
        CheckoutData.FIRST_NAME, CheckoutData.LAST_NAME, CheckoutData.POSTAL_CODE
    )
    checkout.continue_to_overview()

    # When the user clicks Cancel
    inventory = checkout.cancel()

    # Then the inventory page is displayed
    assert inventory.is_loaded()
    assert InventoryPage.URL_FRAGMENT in inventory.get_current_url()
