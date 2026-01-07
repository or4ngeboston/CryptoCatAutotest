from .base_page import BasePage
from playwright.sync_api import Page
import os

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/admin/login"
        self.email_input = page.locator('[id="data.email"]')
        self.password_input = page.locator('[id="data.password"]')
        self.submit_btn = page.get_by_role("button", name="Sign in")

    def navigate(self):
        return self.page.goto(f"{self.base_url}{self.url}")

    def login(self, email: str = None, password: str = None):
        email = email or os.getenv("ADMIN_EMAIL")
        password = password or os.getenv("ADMIN_PASSWORD")
        
        if not email or not password:
            raise ValueError("ADMIN_EMAIL and ADMIN_PASSWORD must be set in .env file or environment")

        self.navigate()
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_btn.click()
        self.page.wait_for_url(f"{self.base_url}/admin", timeout=15000)
