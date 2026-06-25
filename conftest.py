import pytest
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------
# AI Analyst Plugin — auto-activates if API key set
# ------------------------------------------------

def pytest_configure(config):
    """Register AI analyst plugin at session start."""
    from ai_analyst.pytest_plugin import AIAnalystPlugin
    config.pluginmanager.register(AIAnalystPlugin(), "ai_analyst")


# ------------------------------------------------
# Browser & Page Fixtures
# ------------------------------------------------

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
    }

@pytest.fixture(scope="function")
def page(page):
    page.set_default_timeout(10000)
    yield page

# ------------------------------------------------
# App Config Fixtures
# ------------------------------------------------

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com")

@pytest.fixture(scope="session")
def valid_credentials():
    return {
        "username": os.getenv("VALID_USERNAME", "standard_user"),
        "password": os.getenv("VALID_PASSWORD", "secret_sauce"),
    }

@pytest.fixture(scope="session")
def locked_credentials():
    return {
        "username": os.getenv("LOCKED_USERNAME", "locked_out_user"),
        "password": os.getenv("VALID_PASSWORD", "secret_sauce"),
    }

@pytest.fixture(scope="function")
def logged_in_page(page, base_url):
    """Returns a page already logged in as standard_user."""
    from pages.login_page import LoginPage
    LoginPage(page, base_url).login("standard_user", "secret_sauce")
    return page
