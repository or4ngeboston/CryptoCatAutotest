from .base_page import BasePage
from playwright.sync_api import Page
from .components.wallet_modal import WalletModal

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/"
        
        # Selectors
        self.staking_link = page.locator("a[href='/staking']")
        self.how_to_buy_link = page.locator("a[href='/how-to-buy']")
        self.buy_now_header_btn = page.locator("button:has-text('Buy Now')")
        self.buy_with_crypto_btn = page.locator("button:has-text('Buy With Crypto')")
        self.presale_widget = page.locator(".styles_presaleWidget__M4_rI") # Updated based on typical class patterns seen
        
        self.wallet_modal = WalletModal(page)

    def navigate(self):
        return super().navigate(self.url)

    def click_buy_with_crypto(self):
        self.buy_with_crypto_btn.click()
        return self.wallet_modal

    def go_to_staking(self):
        self.staking_link.click()
        from .staking_page import StakingPage
        return StakingPage(self.page)
