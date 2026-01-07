from playwright.sync_api import Page, Response
from typing import Optional

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://admin.cryptocat.ssd.uz"

    def navigate(self, path: str = "") -> Optional[Response]:
        """Navigates to the specified path relative to the base URL."""
        return self.page.goto(f"{self.base_url}{path}")

    def wait_for_load_state(self, state: str = "networkidle"):
        """Waits for the page to reach a specific load state."""
        self.page.wait_for_load_state(state)

    def get_title(self) -> str:
        """Returns the page title."""
        return self.page.title()

    def screenshot(self, name: str):
        """Takes a screenshot and saves it with the given name."""
        self.page.screenshot(path=f"{name}.png")
