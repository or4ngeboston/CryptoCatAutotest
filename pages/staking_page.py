from .base_page import BasePage
from playwright.sync_api import Page

class StakingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/staking"
        
        # Selectors
        self.withdraw_btn = page.locator("button:has-text('Withdraw Staked Tokens')")
        self.buy_and_stake_btn = page.locator("button:has-text('Buy And Stake')")
        self.claim_rewards_btn = page.locator("button:has-text('Claim Rewards')")
        self.staked_balance = page.locator("div:has-text('STAKED BALANCE') + div")
        self.estimated_rewards = page.locator("div:has-text('ESTIMATED REWARDS') + div")

    def navigate(self):
        return super().navigate(self.url)

    def get_staked_balance(self) -> str:
        return self.staked_balance.inner_text()
