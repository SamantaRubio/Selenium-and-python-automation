"""US-001 - Successful Login.

As a customer, I want to log into SauceDemo with valid credentials,
so that I can access the products page.
"""
import pytest

from config.config import Credentials
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.login
def test_successful_login_redirects_to_inventory(login_page):
    """Valid credentials authenticate the user and open the products page."""
    # When the user logs in with valid credentials
    inventory = login_page.login(Credentials.STANDARD_USER, Credentials.PASSWORD)

    # Then the products page is displayed with the inventory list visible
    assert inventory.is_loaded(), "Inventory list should be visible after login"
    # And the URL should contain "/inventory.html"
    assert InventoryPage.URL_FRAGMENT in inventory.get_current_url()
