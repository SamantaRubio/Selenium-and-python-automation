"""Reusable component for the burger side menu.

The side menu is available on every authenticated page (inventory, cart,
checkout), so it is modelled as a standalone component rather than being
duplicated across page objects.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class MenuComponent(BasePage):
    """Controls the slide-out navigation menu."""

    BURGER_BUTTON = (By.ID, "react-burger-menu-btn")
    CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_LINK = (By.ID, "reset_sidebar_link")

    def open_menu(self) -> "MenuComponent":
        """Open the menu and wait for the logout link to become clickable."""
        self.click(self.BURGER_BUTTON)
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
        return self

    def logout(self) -> None:
        """Open the menu and click Logout.

        Menu links use a JavaScript click because the animated side menu does
        not reliably respond to native WebDriver clicks.
        """
        self.open_menu()
        self.click_js(self.LOGOUT_LINK)

    def reset_app_state(self) -> None:
        """Open the menu and click Reset App State."""
        self.open_menu()
        self.click_js(self.RESET_LINK)
