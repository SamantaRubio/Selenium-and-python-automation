"""Central configuration and test data for the SauceDemo test suite.

Credentials are treated as SECRETS: they are never hard-coded here. They must
be provided through the environment - locally via a git-ignored ``.env`` file
(copy ``.env.example`` to ``.env`` and fill it in), and in CI via GitHub
Actions Secrets. If a required secret is missing, the suite fails fast with a
clear message instead of running with a wrong or empty value.

Non-secret settings (base URL, browser, timeouts) keep sensible defaults so
they don't need to be configured for a normal run.
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


def _require_secret(key: str) -> str:
    """Read a required secret from the environment, or fail with guidance.

    Used for sensitive values that must never live in the codebase. Raising
    here (rather than defaulting) guarantees a real, intentional value is
    always supplied - the core of correct secret handling.
    """
    value = os.getenv(key)
    if not value:
        raise RuntimeError(
            f"Missing required secret '{key}'. "
            "Copy .env.example to .env and fill it in (see the README), "
            "or set it as a GitHub Actions Secret in CI."
        )
    return value


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
    """Login accounts, treated as secrets.

    Real account credentials have NO defaults: they must be supplied via the
    environment (.env locally, GitHub Actions Secrets in CI). This keeps
    sensitive data out of the repository entirely.
    """

    # Real accounts - required secrets (no defaults).
    STANDARD_USER = _require_secret("SAUCE_USERNAME")
    PASSWORD = _require_secret("SAUCE_PASSWORD")
    LOCKED_OUT_USER = _require_secret("SAUCE_LOCKED_OUT_USER")
    PROBLEM_USER = _require_secret("SAUCE_PROBLEM_USER")

    # Intentionally invalid values for negative login scenarios. These are
    # deliberately fake (they must NOT match a real account), so they are not
    # secrets and can keep defaults.
    INVALID_USER = os.getenv("SAUCE_INVALID_USER", "invalid_user")
    INVALID_PASSWORD = os.getenv("SAUCE_INVALID_PASSWORD", "wrong_password")


class CheckoutData:
    """Sample data used to complete the checkout form."""

    FIRST_NAME = "John"
    LAST_NAME = "Doe"
    POSTAL_CODE = "12345"
