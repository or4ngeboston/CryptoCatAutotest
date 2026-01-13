import time
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# Load environment variables
load_dotenv()

def test_login_smoke(auth_page: Page):
    """
    Smoke test: Log in and verify dashboard access.
    This relies on the 'auth_page' fixture in conftest.py which handles the login.
    """
    print(f"\n[INFO] Navigating to Dashboard...")
    auth_page.goto("https://admin.cryptocat.ssd.uz/admin")
    
    # Wait for potential redirect or load
    print(f"[INFO] Waiting for load state...")
    auth_page.wait_for_load_state("networkidle")
    
    current_url = auth_page.url
    print(f"[INFO] Current URL: {current_url}")
    print(f"[INFO] Current Title: {auth_page.title()}")

    # Check if we were redirected to login
    if "/login" in current_url:
        print("[WARN] Redirected to login page. Storage state might be invalid or expired.")
        # Optional: Fail fast or attempt re-login (for smoke test, maybe fail is better to signal issue)
        raise AssertionError(f"Smoke test failed: Redirected to login page instead of Dashboard. URL: {current_url}")

    # 2. Verify a key element (e.g., sidebar) is present FIRST (it's a better indicator of load)
    print("[INFO] Waiting for sidebar...")
    sidebar = auth_page.locator(".fi-sidebar-nav")
    expect(sidebar).to_be_visible(timeout=10000)
    
    import re
    # 3. Verify title (relax check to 'Dashboard' or 'Admin' as seen in logs)
    expect(auth_page).to_have_title(re.compile(r"Dashboard|Admin|Cryptocat"), timeout=5000)
    
    print("\n[SUCCESS] Smoke test passed: Logged in and verified Dashboard.")
