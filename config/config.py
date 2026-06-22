"""Central configuration and test data for the SauceDemo test suite.

Values can be overridden through environment variables so the same suite can
run locally and in CI without code changes.
"""
import os


class Config:
    """Global framework configuration."""

    # Application under test
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
    INVENTORY_URL = BASE_URL + "inventory.html"

    # Name of the client-side cookie SauceDemo uses to track the session.
    # Used for fast, programmatic authentication (see utils/session.py).
    SESSION_COOKIE = "session-username"

    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    # Headless is enabled by default in CI; set HEADLESS=false to watch the run.
    HEADLESS = os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes")

    # Timeouts (seconds)
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))


class Credentials:
    """Test accounts provided by SauceDemo."""

    STANDARD_USER = "standard_user"
    LOCKED_OUT_USER = "locked_out_user"
    PROBLEM_USER = "problem_user"
    PASSWORD = "secret_sauce"

    # Intentionally invalid credentials for negative login scenarios.
    INVALID_USER = "invalid_user"
    INVALID_PASSWORD = "wrong_password"


class CheckoutData:
    """Sample data used to complete the checkout form."""

    FIRST_NAME = "John"
    LAST_NAME = "Doe"
    POSTAL_CODE = "12345"
