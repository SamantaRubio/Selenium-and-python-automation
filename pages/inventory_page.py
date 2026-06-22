"""Page object for the SauceDemo Inventory (Products) page."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.components.menu_component import MenuComponent


class InventoryPage(BasePage):
    """Represents the products listing and its shopping interactions."""

    URL_FRAGMENT = "/inventory.html"

    # Sort dropdown option values (the value attribute of each <option>).
    SORT_NAME_AZ = "az"
    SORT_NAME_ZA = "za"
    SORT_PRICE_LOW_HIGH = "lohi"
    SORT_PRICE_HIGH_LOW = "hilo"

    # Locators
    INVENTORY_CONTAINER = (By.CSS_SELECTOR, "[data-test='inventory-list']")
    INVENTORY_ITEM = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_DESC = (By.CSS_SELECTOR, "[data-test='inventory-item-desc']")
    ITEM_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    ITEM_IMAGE = (By.CSS_SELECTOR, ".inventory_item_img img")
    ITEM_BUTTON = (By.CSS_SELECTOR, "button")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")

    def __init__(self, driver):
        super().__init__(driver)
        self.menu = MenuComponent(driver)

    # --- State checks -----------------------------------------------------
    def is_loaded(self) -> bool:
        """Return True once the inventory list is visible."""
        return self.is_visible(self.INVENTORY_CONTAINER)

    # --- Product reads ----------------------------------------------------
    def get_product_count(self) -> int:
        return len(self.find_all(self.INVENTORY_ITEM))

    def get_product_names(self) -> list:
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_product_prices(self) -> list:
        """Return product prices as floats, preserving display order."""
        return [
            float(el.text.replace("$", "")) for el in self.find_all(self.ITEM_PRICE)
        ]

    def get_first_product_details(self) -> dict:
        """Return the displayed attributes of the first product card.

        Used to assert that each product exposes image, name, description,
        price and an action button.
        """
        item = self.find_all(self.INVENTORY_ITEM)[0]
        return {
            "name": item.find_element(*self.ITEM_NAME).text,
            "description": item.find_element(*self.ITEM_DESC).text,
            "price": item.find_element(*self.ITEM_PRICE).text,
            "has_image": bool(item.find_elements(*self.ITEM_IMAGE)),
            "button_text": item.find_element(*self.ITEM_BUTTON).text,
        }

    def each_product_is_complete(self) -> bool:
        """Verify every product card contains all expected attributes."""
        for item in self.find_all(self.INVENTORY_ITEM):
            has_image = bool(item.find_elements(*self.ITEM_IMAGE))
            has_name = bool(item.find_element(*self.ITEM_NAME).text)
            has_desc = bool(item.find_element(*self.ITEM_DESC).text)
            has_price = item.find_element(*self.ITEM_PRICE).text.startswith("$")
            has_button = bool(item.find_element(*self.ITEM_BUTTON).text)
            if not all([has_image, has_name, has_desc, has_price, has_button]):
                return False
        return True

    # --- Sorting ----------------------------------------------------------
    def sort_products(self, option_value: str) -> "InventoryPage":
        """Select a sort option by its value (use the SORT_* constants)."""
        self.select_by_value(self.SORT_DROPDOWN, option_value)
        return self

    # --- Cart actions -----------------------------------------------------
    def _item_button(self, product_name: str) -> tuple:
        """Build a locator for the action button inside a product's card.

        Matching by the visible product name keeps the locator independent of
        the button's add/remove state.
        """
        xpath = (
            f"//div[@class='inventory_item']"
            f"[.//*[@data-test='inventory-item-name' and text()={self._xpath_literal(product_name)}]]"
            f"//button"
        )
        return (By.XPATH, xpath)

    @staticmethod
    def _xpath_literal(value: str) -> str:
        """Safely quote a string for use inside an XPath expression."""
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat('" + "', \"'\", '".join(parts) + "')"

    def add_product_to_cart(self, product_name: str) -> "InventoryPage":
        self.click(self._item_button(product_name))
        return self

    def remove_product_from_cart(self, product_name: str) -> "InventoryPage":
        self.click(self._item_button(product_name))
        return self

    def get_product_button_text(self, product_name: str) -> str:
        return self.get_text(self._item_button(product_name))

    def get_cart_badge_count(self) -> int:
        """Return the cart badge number, or 0 when the badge is not shown."""
        if not self.is_present(self.CART_BADGE):
            return 0
        return int(self.find(self.CART_BADGE).text)

    def is_cart_badge_visible(self) -> bool:
        return self.is_present(self.CART_BADGE)

    # --- Navigation -------------------------------------------------------
    def go_to_cart(self) -> CartPage:
        self.click(self.CART_LINK)
        return CartPage(self.driver)
