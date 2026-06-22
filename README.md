# SauceDemo - Selenium + Python Automation

[![CI](https://github.com/SamantaRubio/Selenium-and-python-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/SamantaRubio/Selenium-and-python-automation/actions/workflows/ci.yml)

End-to-end UI test automation for [SauceDemo](https://www.saucedemo.com/),
built with **Selenium WebDriver**, **Python** and **pytest**, following the
**Page Object Model (POM)** design pattern.

## Highlights

- **Page Object Model** - every page is a class; tests never touch raw selectors.
- **Reusable `BasePage`** - all Selenium calls (waits, clicks, typing) live in one place.
- **Explicit waits everywhere** - no fragile `time.sleep`; reliable on slow loads.
- **Stable locators** - prefers SauceDemo's `data-test` attributes.
- **Component objects** - the shared burger menu is modelled once and reused.
- **Fast, isolated auth** - tests authenticate by injecting the session cookie
  instead of repeating the UI login; the UI login itself is tested in isolation.
- **Configurable** - browser, headless mode and timeouts via environment variables.
- **Traceable** - each test maps to a user story and is tagged with a pytest marker.
- **Screenshots on failure** - captured automatically into `reports/screenshots/`.
- **HTML report** - generated at `reports/report.html` after each run.

## Project Structure

```
.
├── config/
│   └── config.py             # URLs, credentials, test data, timeouts
├── pages/                    # Page Object Model
│   ├── base_page.py          # Shared Selenium interactions
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── components/
│       └── menu_component.py # Reusable burger-menu component
├── tests/                    # One test module per user story (US-001..US-011)
├── utils/
│   ├── driver_factory.py     # WebDriver creation (Chrome / Firefox)
│   └── session.py            # Programmatic (cookie-based) authentication
├── docs/user-stories/        # Source acceptance criteria
├── conftest.py               # Fixtures + screenshot-on-failure hook
├── pytest.ini                # Pytest config and markers
└── requirements.txt
```

## Setup

Requires Python 3.9+ and Google Chrome (installed). Selenium 4 downloads the
matching driver automatically via Selenium Manager - no manual setup needed.

```bash
# From the project root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Tests

> Activate the virtual environment first: `source .venv/bin/activate`

### Run everything

```bash
# Full suite, with a visible browser window
pytest

# Full suite, headless (no visible browser) - ideal for CI
HEADLESS=true pytest
```

### Run a subset

```bash
# A single user story (one file)
pytest tests/test_us001_login.py

# A single test function within a file
pytest tests/test_us004_sort_products.py::test_sort_price_low_to_high

# A group of stories by marker
pytest -m smoke        # critical happy-path checks
pytest -m login        # US-001 / US-002
pytest -m products     # US-003 / US-004
pytest -m cart         # US-005 / US-006 / US-007
pytest -m checkout     # US-008 / US-009
pytest -m session      # US-010 / US-011

# Combine markers (logical OR / AND / NOT)
pytest -m "cart or checkout"
pytest -m "products and not smoke"

# Filter by name fragment instead of marker
pytest -k "logout"
pytest -k "sort and price"
```

### Choose the browser

```bash
# Chrome is the default
pytest

# Run on Firefox instead
BROWSER=firefox pytest

# Firefox, headless
BROWSER=firefox HEADLESS=true pytest
```

### Useful run modes

```bash
# Stop at the first failure
pytest -x

# Re-run only the tests that failed last time
pytest --lf

# Show print/logging output live
pytest -s

# Quieter or more verbose output
pytest -q
pytest -vv

# Point the suite at a different environment
BASE_URL=https://www.saucedemo.com/ pytest

# Increase waits on a slow connection
EXPLICIT_WAIT=20 PAGE_LOAD_TIMEOUT=60 pytest
```

### Parallel execution (optional)

Speeds up the suite by running tests across multiple browser sessions.
Requires the extra plugin: `pip install pytest-xdist`.

```bash
# Use all available CPU cores
HEADLESS=true pytest -n auto

# Use a fixed number of workers
HEADLESS=true pytest -n 4
```

### Reports & artifacts

- An HTML report is generated at `reports/report.html` after every run.
- A screenshot of any failing test is saved to `reports/screenshots/`.

```bash
# Open the HTML report (macOS)
open reports/report.html
```

## Configuration

Override any of these via environment variables:

| Variable           | Default                       | Description                         |
|--------------------|-------------------------------|-------------------------------------|
| `BASE_URL`         | `https://www.saucedemo.com/`  | Application under test              |
| `BROWSER`          | `chrome`                      | `chrome` or `firefox`               |
| `HEADLESS`         | `false`                       | Run without a visible browser       |
| `EXPLICIT_WAIT`    | `10`                          | Max seconds for element waits       |
| `PAGE_LOAD_TIMEOUT`| `30`                          | Max seconds for page loads          |

## Design Notes

### Authentication strategy

Every test runs in a **fresh, isolated browser session** (the `driver` fixture
creates and quits a browser per test), so no state ever leaks between tests -
they can run in any order or in parallel.

For tests that simply *need to be logged in* (everything except the login
stories), authentication is done **programmatically** by injecting SauceDemo's
`session-username` cookie (`utils/session.py`) instead of driving the UI login.
This follows the widely recommended pattern - *don't log in through the UI on
every test*:

- **The UI login is a feature**, tested on its own in US-001 / US-002. Re-running
  it as setup for every other test adds no coverage, only runtime and a shared
  point of failure.
- **Faster suite** - each authenticated test skips ~2s of typing and redirects.
- **Still fully isolated** - the browser is brand new every time.

The `LoginPage` object is still used directly by the login tests, so the real
UI flow remains covered.

## Continuous Integration

Every push and pull request to `main` runs the full suite on
**GitHub Actions** (`.github/workflows/ci.yml`):

- Runs **headless** across a Python matrix (3.10 / 3.11 / 3.12).
- Caches pip dependencies for faster builds.
- Uses the Chrome pre-installed on the runner; Selenium Manager resolves the
  driver automatically.
- Publishes the HTML report and any failure screenshots as **downloadable
  artifacts**, even when the run fails.
- Can also be triggered manually from the Actions tab (`workflow_dispatch`).

## User Story Coverage

| Story  | Description            | Test module                          |
|--------|------------------------|--------------------------------------|
| US-001 | Successful login       | `test_us001_login.py`                |
| US-002 | Invalid login          | `test_us002_invalid_login.py`        |
| US-003 | View products          | `test_us003_view_products.py`        |
| US-004 | Sort products          | `test_us004_sort_products.py`        |
| US-005 | Add product to cart    | `test_us005_add_product_cart.py`     |
| US-006 | Remove product         | `test_us006_remove_product_cart.py`  |
| US-007 | View cart              | `test_us007_view_cart.py`            |
| US-008 | Complete checkout      | `test_us008_checkout.py`             |
| US-009 | Cancel checkout        | `test_us009_cancel_checkout.py`      |
| US-010 | Logout                 | `test_us010_logout.py`               |
| US-011 | Reset app state        | `test_us011_reset_app_state.py`      |
