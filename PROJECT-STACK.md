# Project Stack

The complete technology stack behind this SauceDemo automation framework, and
the reasoning behind each choice. Python packages are installed via
[`requirements.txt`](requirements.txt); this document covers the whole stack,
including the parts that aren't pip dependencies (browser, CI, patterns).

## At a glance

| Layer | Technology | Version |
|-------|------------|---------|
| Language | Python | 3.9+ (CI runs 3.10 / 3.11 / 3.12) |
| Browser automation | Selenium WebDriver | >= 4.18 |
| Driver management | Selenium Manager | bundled with Selenium 4 |
| Test runner | pytest | >= 8.0 |
| Reporting | pytest-html | >= 4.1 |
| Parallel execution (optional) | pytest-xdist | >= 3.5 |
| Design pattern | Page Object Model (POM) | — |
| Browser | Google Chrome (Firefox supported) | — |
| CI/CD | GitHub Actions | — |
| Version control | Git + GitHub | — |

## Details and rationale

### Language — Python 3.9+
Readable, concise, and backed by a first-class testing ecosystem. The suite
targets 3.9+ and is verified in CI across Python 3.10, 3.11 and 3.12 to catch
version-specific issues.

### Browser automation — Selenium WebDriver (>= 4.18)
The industry standard for driving real browsers. Language-agnostic, W3C-based,
and supports every major browser and remote grids. The natural fit for
end-to-end UI testing.

### Driver management — Selenium Manager
Bundled with Selenium 4. Detects the installed browser and downloads the
matching driver automatically, so there is no `chromedriver` binary to commit
or version to maintain — especially valuable in CI.

### Test runner — pytest (>= 8.0)
The most powerful Python test framework. Provides the features this framework
relies on: fixtures (setup/teardown), markers (grouping/filtering),
parametrization, hooks, and clean assertion introspection.

### Reporting — pytest-html (>= 4.1)
Generates a self-contained HTML report (`reports/report.html`) after each run,
easy to open or publish as a CI artifact.

### Parallel execution (optional) — pytest-xdist (>= 3.5)
Runs tests across multiple CPU cores (`pytest -n auto`). Optional because the
framework's per-test isolation already makes it safe to parallelize; enable it
when the suite grows. Commented out in `requirements.txt` by default.

### Design pattern — Page Object Model (POM)
Each page/component is a class exposing locators and business actions; a shared
`BasePage` centralizes all Selenium mechanics. Keeps tests readable and
maintenance localized when the UI changes.

### Browser — Google Chrome (Firefox supported)
Chrome is the default; the `driver_factory` also supports Firefox via the
`BROWSER` environment variable. Runs headless in CI.

### CI/CD — GitHub Actions
Runs the full suite headless on every push and pull request, across a Python
version matrix, caching dependencies and publishing reports/screenshots as
artifacts. The `main` branch is protected: merges require a green run.

### Version control — Git + GitHub
Source control and collaboration; hosts the CI pipeline and branch-protection
rules.

## Standard library (no install needed)

The framework also uses Python built-ins: `os` (environment variables and
paths in `config/config.py`) and `time` where needed. These ship with Python
and are not listed in `requirements.txt`.
