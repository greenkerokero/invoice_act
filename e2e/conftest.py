import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:10000"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser, base_url):
    context = browser.new_context()
    page = context.new_page()
    original_goto = page.goto
    page.goto = lambda url, **kwargs: original_goto(f"{base_url}{url}", **kwargs)
    yield page
    context.close()
