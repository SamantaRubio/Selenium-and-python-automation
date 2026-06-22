"""Page object for the SauceDemo Cart page."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    """Represents the shopping cart and its actions."""

    URL_FRAGMENT = "/cart.html"

    CART_ITEM = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "[data-test='continue-shopping']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.cart_button")

    def is_loaded(self) -> bool:
        return self.wait_for_url_contains(self.URL_FRAGMENT)

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEM))

    def get_item_names(self) -> list:
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAME)]

    def contains_product(self, product_name: str) -> bool:
        return product_name in self.get_item_names()

    def get_cart_badge_count(self) -> int:
        if not self.is_present(self.CART_BADGE):
            return 0
        return int(self.find(self.CART_BADGE).text)

    def proceed_to_checkout(self) -> CheckoutPage:
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.driver)
