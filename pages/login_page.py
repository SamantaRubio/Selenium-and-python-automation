"""Page object for the SauceDemo Login page."""
from selenium.webdriver.common.by import By

from config.config import Config
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    """Represents the login screen and its authentication actions."""

    # Locators (data-test attributes are the most stable selectors on SauceDemo)
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self) -> "LoginPage":
        """Open the login page."""
        self.open(Config.BASE_URL)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> InventoryPage:
        """Perform a full login and return the resulting Inventory page.

        Use this for the happy path; the returned page object assumes
        authentication succeeded.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return InventoryPage(self.driver)

    def get_error_message(self) -> str:
        """Return the text of the login error banner."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
