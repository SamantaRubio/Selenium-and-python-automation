"""Programmatic authentication helper.

Best practice for E2E suites: keep every test fully isolated (a fresh browser
per test) but DO NOT log in through the UI on every test. The UI login is slow
and is already verified by its own tests (US-001 / US-002); repeating it as
setup for every other test just adds runtime and a shared failure point.

Instead we establish the authenticated session directly by injecting
SauceDemo's session cookie, then land on the inventory page. This gives the
best of both worlds: isolation (no shared/leaked state between tests) and
speed (no repeated UI typing and redirects).
"""
from config.config import Config
from pages.inventory_page import InventoryPage


def login_with_session(driver, username: str) -> InventoryPage:
    """Authenticate ``username`` by injecting the session cookie.

    Returns the Inventory page object, ready to use.
    """
    # A cookie can only be set for a domain the browser is currently on,
    # so we must visit the site before adding the cookie.
    driver.get(Config.BASE_URL)
    driver.add_cookie({"name": Config.SESSION_COOKIE, "value": username})

    # Reload directly into the authenticated area now that the cookie is set.
    driver.get(Config.INVENTORY_URL)
    return InventoryPage(driver)
