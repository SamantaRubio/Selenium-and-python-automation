"""Central configuration and test data for the SauceDemo test suite.

Values can be overridden through environment variables so the same suite can
run locally and in CI without code changes.

Note on credentials: SauceDemo's logins are *public demo credentials* (printed
on the login page), so they are safe to keep as defaults. Even so, they are
read via environment variables to model the correct practice - real secrets
must never be hard-coded; they belong in env vars / a .env file (git-ignored)
or a secrets manager, and in CI in GitHub Actions Secrets.
"""
import os


def _load_dotenv() -> None:
    """Load key=value pairs from a local .env file, if present.

    Kept dependency-free on purpose: values already set in the real
    environment always win, so this never overrides CI-provided secrets.
    """
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


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
    """SauceDemo test accounts.

    These are public demo credentials; the env-var lookups exist to demonstrate
    the secure pattern and to allow overriding without touching the code.
    """

    STANDARD_USER = os.getenv("SAUCE_USERNAME", "standard_user")
    PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
    LOCKED_OUT_USER = os.getenv("SAUCE_LOCKED_OUT_USER", "locked_out_user")
    PROBLEM_USER = os.getenv("SAUCE_PROBLEM_USER", "problem_user")

    # Intentionally invalid credentials for negative login scenarios.
    INVALID_USER = os.getenv("SAUCE_INVALID_USER", "invalid_user")
    INVALID_PASSWORD = os.getenv("SAUCE_INVALID_PASSWORD", "wrong_password")


class CheckoutData:
    """Sample data used to complete the checkout form."""

    FIRST_NAME = "John"
    LAST_NAME = "Doe"
    POSTAL_CODE = "12345"
