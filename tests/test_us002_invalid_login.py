"""US-002 - Invalid Login.

As a customer, I want to receive an error message when I use invalid
credentials, so that I know my login attempt failed.
"""
import pytest

from config.config import Credentials
from pages.login_page import LoginPage


@pytest.mark.login
def test_invalid_login_shows_error(login_page):
    """Invalid credentials keep the user on the login page with an error."""
    # When the user submits invalid credentials
    login_page.enter_username(Credentials.INVALID_USER)
    login_page.enter_password(Credentials.INVALID_PASSWORD)
    login_page.click_login()

    # Then an error message should be displayed
    assert login_page.is_error_displayed(), "An error message should be shown"
    assert "Username and password do not match" in login_page.get_error_message()

    # And the user should remain on the login page (not redirected to inventory)
    assert "/inventory.html" not in login_page.get_current_url()
    assert LoginPage.LOGIN_BUTTON  # login form is still present


@pytest.mark.login
def test_locked_out_user_is_rejected(login_page):
    """A locked-out account cannot access the products page."""
    login_page.enter_username(Credentials.LOCKED_OUT_USER)
    login_page.enter_password(Credentials.PASSWORD)
    login_page.click_login()

    assert login_page.is_error_displayed()
    assert "locked out" in login_page.get_error_message().lower()
    assert "/inventory.html" not in login_page.get_current_url()
