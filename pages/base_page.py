"""Base page object shared by every page in the suite.

Centralises all low-level Selenium interactions (waits, clicks, typing, reads)
so that concrete page objects stay focused on business behaviour and never
touch the WebDriver API directly. This keeps the page objects clean and makes
the framework resilient to timing issues through consistent explicit waits.
"""
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from config.config import Config


class BasePage:
    """Common behaviour inherited by all page objects."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    # --- Navigation -------------------------------------------------------
    def open(self, url: str) -> None:
        """Navigate the browser to the given URL."""
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # --- Element interactions --------------------------------------------
    def find(self, locator: tuple) -> WebElement:
        """Return a single element once it is present in the DOM."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: tuple) -> list:
        """Return all matching elements once at least one is present."""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple) -> None:
        """Wait until the element is clickable, then click it."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def click_js(self, locator: tuple) -> None:
        """Click an element via JavaScript.

        Needed for animated widgets (e.g. the react-burger-menu side menu),
        whose links do not respond reliably to native WebDriver clicks.
        """
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator: tuple, text: str) -> None:
        """Clear a field and type the given text into it.

        SauceDemo's checkout form fades in, so a field can be visible while
        still mid-animation and reject input ("element not interactable").
        Instead of typing once, we poll: keep re-finding the element and
        retrying until it accepts the input or the wait times out. The
        WebDriverWait polling interval handles the animation settling without
        a hard-coded sleep.
        """

        def _try_type(driver):
            try:
                element = driver.find_element(*locator)
                element.clear()
                element.send_keys(text)
                return element
            except (ElementNotInteractableException, StaleElementReferenceException):
                return False

        self.wait.until(_try_type)

    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element."""
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def select_by_value(self, locator: tuple, value: str) -> None:
        """Select an <option> from a native dropdown by its value attribute."""
        dropdown = Select(self.find(locator))
        dropdown.select_by_value(value)

    # --- State checks -----------------------------------------------------
    def is_visible(self, locator: tuple) -> bool:
        """Return True if the element becomes visible within the wait window."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def is_present(self, locator: tuple) -> bool:
        """Return True if at least one matching element exists in the DOM."""
        return len(self.driver.find_elements(*locator)) > 0

    def wait_for_url_contains(self, fragment: str) -> bool:
        """Wait until the current URL contains the given fragment."""
        return self.wait.until(EC.url_contains(fragment))
