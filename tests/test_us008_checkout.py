"""US-008 - Complete Checkout.

As a customer, I want to complete a purchase, so that I can buy my selected
products.
"""
import pytest

from config.config import CheckoutData

PRODUCT = "Sauce Labs Backpack"


@pytest.mark.smoke
@pytest.mark.checkout
def test_complete_checkout_shows_confirmation(inventory_page):
    """A full checkout flow ends with the order confirmation message."""
    # Given the user has an item in the cart and is on the cart page
    inventory_page.add_product_to_cart(PRODUCT)
    cart = inventory_page.go_to_cart()
    assert cart.contains_product(PRODUCT)

    # When the user checks out, fills in the form and finishes the order
    checkout = cart.proceed_to_checkout()
    checkout.fill_information(
        CheckoutData.FIRST_NAME, CheckoutData.LAST_NAME, CheckoutData.POSTAL_CODE
    )
    checkout.continue_to_overview()
    checkout.finish_order()

    # Then the confirmation message is displayed
    assert checkout.is_order_complete()
    assert checkout.get_confirmation_message() == "Thank you for your order!"


@pytest.mark.checkout
def test_checkout_requires_customer_information(inventory_page):
    """Continuing without customer details surfaces a validation error."""
    inventory_page.add_product_to_cart(PRODUCT)
    checkout = inventory_page.go_to_cart().proceed_to_checkout()

    # Submitting the empty information form should be rejected.
    checkout.continue_to_overview()
    assert "First Name is required" in checkout.get_error_message()
