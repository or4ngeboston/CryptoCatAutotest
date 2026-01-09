import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import Browser, Page

from pages.login_page import LoginPage

load_dotenv()

@pytest.fixture(scope="session")
def auth_storage(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    
    login_page = LoginPage(page)
    login_page.login()
    
    # Save storage state
    auth_storage_file = "auth.json"
    context.storage_state(path=auth_storage_file)
    context.close()
    return auth_storage_file

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, auth_storage):
    return {
        **browser_context_args,
        "storage_state": auth_storage,
        "viewport": {
            "width": 1280,
            "height": 720,
        }
    }

@pytest.fixture
def auth_page(page: Page):
    # Now any 'page' is already authenticated due to browser_context_args
    return page
