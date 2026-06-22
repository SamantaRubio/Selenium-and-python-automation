"""Pytest fixtures and hooks shared across the whole test suite."""
import os

import pytest

from config.config import Credentials
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.driver_factory import create_driver
from utils.session import login_with_session

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "reports", "screenshots")


@pytest.fixture
def driver():
    """Provide a fresh browser session for each test and quit it afterwards."""
    drv = create_driver()
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver) -> LoginPage:
    """Return the Login page already loaded in the browser."""
    return LoginPage(driver).load()


@pytest.fixture
def inventory_page(driver) -> InventoryPage:
    """Return the Inventory page with the standard user already authenticated.

    Authentication is established programmatically (by injecting the session
    cookie) rather than through the UI. This keeps the test isolated with a
    fresh browser while skipping the slow, repetitive UI login - which is its
    own concern, covered by US-001 / US-002. See utils/session.py for details.
    """
    page = login_with_session(driver, Credentials.STANDARD_USER)
    assert page.is_loaded(), "Precondition failed: could not reach the inventory page"
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when a test fails, for easier debugging."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            safe_name = item.name.replace("/", "_").replace("::", "_")
            path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")
            try:
                drv.save_screenshot(path)
                print(f"\nScreenshot saved to: {path}")
            except Exception as exc:  # pragma: no cover - best effort only
                print(f"\nCould not capture screenshot: {exc}")
