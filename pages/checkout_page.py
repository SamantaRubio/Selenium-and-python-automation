"""Page object for the SauceDemo checkout flow.

Covers the three linear steps of the checkout: customer information,
order overview and the completion confirmation.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Represents the multi-step checkout process."""

    STEP_ONE_FRAGMENT = "/checkout-step-one.html"
    STEP_TWO_FRAGMENT = "/checkout-step-two.html"
    COMPLETE_FRAGMENT = "/checkout-complete.html"

    # Step one: customer information form
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE_INPUT = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test='cancel']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Step two: order overview
    FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test='finish']")

    # Completion
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutPage":
        """Complete the customer information form (step one)."""
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def continue_to_overview(self) -> "CheckoutPage":
        """Submit the information form and advance to the overview step."""
        self.click(self.CONTINUE_BUTTON)
        return self

    def finish_order(self) -> "CheckoutPage":
        """Confirm the order on the overview step."""
        self.click(self.FINISH_BUTTON)
        return self

    def get_confirmation_message(self) -> str:
        """Return the completion header text (e.g. 'Thank you for your order!')."""
        return self.get_text(self.COMPLETE_HEADER)

    def is_order_complete(self) -> bool:
        return self.wait_for_url_contains(self.COMPLETE_FRAGMENT)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def cancel(self):
        """Click Cancel and return to the inventory page.

        Cancel on the overview step navigates back to the inventory list.
        Imported lazily to avoid a circular import between page objects.
        """
        from pages.inventory_page import InventoryPage

        self.click(self.CANCEL_BUTTON)
        return InventoryPage(self.driver)
