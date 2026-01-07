from playwright.sync_api import Page

class WalletModal:
    def __init__(self, page: Page):
        self.page = page
        
        # Selectors
        self.modal_container = page.locator(".mantine-Modal-content")
        self.trust_wallet_option = page.locator("div:has-text('Trust Wallet')")
        self.close_button = page.locator("button.styles_closeBtn__yt5mb")
        self.help_button = page.locator("button:has-text(\"I Don't Have A Wallet\")")

    def is_visible(self) -> bool:
        return self.modal_container.is_visible()

    def select_trust_wallet(self):
        self.trust_wallet_option.click()

    def close(self):
        self.close_button.click()
