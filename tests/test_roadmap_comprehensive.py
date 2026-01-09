import time
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# Load environment variables
load_dotenv()

def test_roadmap_comprehensive(auth_page: Page):
    """
    Comprehensive test to create a roadmap and then delete it.
    """
    # 1. Start from dashboard
    auth_page.goto("https://admin.cryptocat.ssd.uz/admin")
    
    # 2. Navigate to Roadmaps tab
    print("\n[STEP 1] Navigating to Roadmaps...")
    roadmaps_link = auth_page.locator("a.fi-sidebar-item-button").filter(has_text="Roadmaps")
    roadmaps_link.click()
    auth_page.wait_for_url("**/admin/roadmaps**")
    
    # 3. Click New Roadmap button
    print("[STEP 2] Creating a new roadmap...")
    create_button = auth_page.locator("button, a").filter(has_text="New roadmap").first
    create_button.click()
    
    # 4. Fill in the form
    timestamp = int(time.time())
    test_date = f"Test Date {timestamp}"
    test_body = f"This is a test roadmap body created at {timestamp}."
    
    # Date field
    date_input = auth_page.locator('#mountedActionsData\\.0\\.date')
    expect(date_input).to_be_visible()
    date_input.fill(test_date)
    print(f"[OK] Filled date: {test_date}")
    
    # Body field (Rich Text Editor / ProseMirror)
    # Based on exploration, the editor is a TipTap/ProseMirror instance
    # It's better to click/focus and type for rich text editors
    body_editor = auth_page.locator('.tiptap.ProseMirror').first
    expect(body_editor).to_be_visible()
    body_editor.click()
    body_editor.press_sequentially(test_body)
    print(f"[OK] Filled body content")
    
    # 5. Submit the form
    submit_button = auth_page.locator('button[type="submit"]').filter(has_text="Create").first
    submit_button.click()
    print("[OK] Clicked Create button")
    
    # 6. Verify creation
    # Wait for success notification and modal to close
    auth_page.wait_for_timeout(2000)
    
    # Search for the roadmap to verify it exists
    print("\n[STEP 3] Verifying roadmap creation...")
    search_input = auth_page.locator("input[placeholder*='Search']").first
    search_input.fill(test_date)
    search_input.press("Enter")
    auth_page.wait_for_timeout(2000)
    
    # Verify it appears in the table
    roadmap_row = auth_page.locator("table tr").filter(has_text=test_date).first
    expect(roadmap_row).to_be_visible()
    print(f"[OK] Roadmap '{test_date}' found in the list.")
    
    # 7. Delete the roadmap
    print(f"\n[STEP 4] Deleting the roadmap '{test_date}'...")
    
    # Click on the Delete button in the table row
    print(f"Clicking Delete button for roadmap '{test_date}' in table row...")
    delete_btn = roadmap_row.locator("button, a").filter(has_text="Delete").first
    expect(delete_btn).to_be_visible()
    delete_btn.click()
    
    # Handle Confirmation Modal
    print("Waiting for confirmation modal...")
    # Confirmation modal is usually a global modal with a "Confirm" button
    confirm_btn = auth_page.locator(".fi-modal").locator("button").filter(has_text="Confirm").filter(visible=True).first
    expect(confirm_btn).to_be_visible()
    confirm_btn.click()
    
    # 8. Final Verification
    print("\n[STEP 5] Verifying deletion...")
    auth_page.wait_for_timeout(2000)
    
    # Search again
    search_input.fill(test_date)
    search_input.press("Enter")
    auth_page.wait_for_timeout(3000)
    
    # The list should be empty or show "No results"
    # Filament usually shows "No roadmaps" or similar
    empty_state = auth_page.get_by_text("No roadmaps", exact=False).or_(auth_page.get_by_text("No results", exact=False))
    
    if empty_state.count() > 0:
        print("[OK] Empty state visible.")
    else:
        # Check that the table does not contain the test date
        expect(auth_page.locator("table")).not_to_contain_text(test_date)
    
    print(f"[SUCCESS] Roadmap '{test_date}' is definitively gone.")
