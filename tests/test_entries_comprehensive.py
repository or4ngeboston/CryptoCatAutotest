import time
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# Load environment variables
load_dotenv()

def test_entries_comprehensive(auth_page: Page):
    """
    Comprehensive test to edit an entry and then revert it.
    """
    # 1. Start from dashboard
    auth_page.goto("https://admin.cryptocat.ssd.uz/admin")
    
    # 2. Navigate to Entries tab
    print("\n[STEP 1] Navigating to Entries...")
    entries_link = auth_page.locator("a.fi-sidebar-item-button").filter(has_text="Entries")
    entries_link.click()
    auth_page.wait_for_url("**/admin/entries**")
    
    # 3. Find "Main page Title" entry
    print("[STEP 2] Finding 'Main page Title' entry...")
    # Search for it to be sure it's on the first page
    search_input = auth_page.locator("input[placeholder*='Search']").first
    search_input.fill("Main page Title")
    search_input.press("Enter")
    auth_page.wait_for_timeout(2000)
    
    entry_row = auth_page.locator("table tr").filter(has_text="Main page Title").first
    expect(entry_row).to_be_visible()
    
    # 4. Click row to edit
    entry_row.click()
    print("[OK] Clicked row to open edit modal")
    
    # 5. Fill in the form
    timestamp = int(time.time())
    new_body = f"Title {timestamp}"
    
    # Body fields are textareas. We'll find the one for English (usually the first 'body' one)
    # Using the suspected ID pattern for Filament
    body_field = auth_page.locator('textarea[id$=".body"]').first
    if not body_field.is_visible():
         body_field = auth_page.locator('textarea').filter(has_text="").first # fallback
    
    expect(body_field).to_be_visible()
    
    original_body = body_field.input_value()
    print(f"[OK] Original body: {original_body}")
    
    body_field.fill(new_body)
    print(f"[OK] Filled new body: {new_body}")
    
    # 6. Save changes
    save_button = auth_page.locator('button[type="submit"]').filter(has_text="Save changes").first
    save_button.click()
    print("[OK] Clicked Save changes button")
    
    # 7. Verify update
    auth_page.wait_for_timeout(3000)
    
    # Check if the text is updated in the table
    # We might need to refresh or search again, but usually Filament updates the row
    expect(auth_page.locator("table")).to_contain_text(new_body)
    print(f"[OK] Verified update: {new_body} found in table")
    
    # 8. Revert changes
    print("\n[STEP 3] Reverting changes...")
    updated_row = auth_page.locator("table tr").filter(has_text="Main page Title").first
    updated_row.click()
    
    body_field = auth_page.locator('textarea[id$=".body"]').first
    expect(body_field).to_be_visible()
    body_field.fill(original_body)
    
    save_button = auth_page.locator('button[type="submit"]').filter(has_text="Save changes").first
    save_button.click()
    auth_page.wait_for_timeout(3000)
    
    expect(auth_page.locator("table")).to_contain_text(original_body)
    print(f"[SUCCESS] Reverted to original body: {original_body}")
