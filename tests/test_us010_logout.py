"""US-010 - Logout.

As a customer, I want to log out, so that I can end my session securely.
"""
import pytest

from pages.login_page import LoginPage


@pytest.mark.session
def test_logout_returns_to_login_page(inventory_page):
    """Logging out via the side menu returns the user to the login page."""
    # When the user opens the side menu and clicks Logout
    inventory_page.menu.logout()

    # Then the login page is displayed (the login button is visible again)
    login = LoginPage(inventory_page.driver)
    assert login.is_visible(LoginPage.LOGIN_BUTTON), "Login form should be visible"

    # And the URL should be back at the site root
    assert login.get_current_url().rstrip("/").endswith("saucedemo.com")
