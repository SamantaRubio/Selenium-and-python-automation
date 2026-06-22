"""WebDriver factory.

Builds a configured WebDriver instance based on the framework configuration.
Selenium 4's built-in Selenium Manager automatically resolves and downloads
the matching browser driver, so no manual driver setup is required.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.config import Config


def create_driver():
    """Create and return a WebDriver instance for the configured browser."""
    if Config.BROWSER == "firefox":
        driver = _create_firefox()
    else:
        driver = _create_chrome()

    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    driver.maximize_window()
    return driver


def _create_chrome():
    options = ChromeOptions()
    if Config.HEADLESS:
        options.add_argument("--headless=new")
    # Stability flags commonly needed in containerised / CI environments.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Suppress Chrome's password manager and the "password found in a data
    # breach / change your password" leak-detection dialog. That dialog is
    # part of the browser chrome (not the page DOM), so it cannot be closed
    # with Selenium once shown - it steals focus and breaks form input.
    # Disabling it at startup keeps the run stable.
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    options.add_argument("--disable-features=PasswordLeakDetection")
    # Hide the "Chrome is being controlled by automated test software" infobar.
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=options)


def _create_firefox():
    options = FirefoxOptions()
    if Config.HEADLESS:
        options.add_argument("--headless")
    return webdriver.Firefox(options=options)
