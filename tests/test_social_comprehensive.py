import os
import time
import tempfile
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# Load environment variables
load_dotenv()

def test_social_comprehensive(auth_page: Page):
    """
    Comprehensive test to create a social link and then delete it.
    """
    # 1. Start from dashboard
    auth_page.goto("https://admin.cryptocat.ssd.uz/admin")
    
    # 2. Navigate to Socials tab
    print("\n[STEP 1] Navigating to Socials...")
    socials_link = auth_page.locator("a.fi-sidebar-item-button").filter(has_text="Socials")
    socials_link.click()
    auth_page.wait_for_url("**/admin/socials**")
    
    # 3. Click New social button
    print("[STEP 2] Creating new social...")
    create_button = auth_page.locator("button, a").filter(has_text="New social").first
    create_button.click()
    
    # 4. Fill in the form
    timestamp = int(time.time())
    test_title = f"Test Social {timestamp}"
    test_link = f"https://example.com/test-{timestamp}"
    
    # Title fields
    auth_page.locator('#mountedActionsData\\.0\\.title').fill(test_title)
    auth_page.locator('#mountedActionsData\\.0\\.title_uz').fill(f"{test_title} UZ")
    auth_page.locator('#mountedActionsData\\.0\\.title_ru').fill(f"{test_title} RU")
    print(f"[OK] Filled titles: {test_title}")
    
    # Link field
    auth_page.locator('#mountedActionsData\\.0\\.link').fill(test_link)
    print(f"[OK] Filled link: {test_link}")
    
    # Icon upload (FilePond)
    temp_dir = tempfile.gettempdir()
    test_icon_path = os.path.join(temp_dir, f"test_social_{timestamp}.png")
    
    # Create a minimal valid PNG file
    png_header = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
        0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
        0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,
        0x54, 0x08, 0xD7, 0x63, 0xF8, 0xFF, 0xFF, 0x3F,
        0x00, 0x05, 0xFE, 0x02, 0xFE, 0xDC, 0x44, 0x74,
        0x8E, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E,
        0x44, 0xAE, 0x42, 0x60, 0x82
    ])
    with open(test_icon_path, 'wb') as f:
        f.write(png_header)
    
    print(f"[OK] Created test icon: {test_icon_path}")
    
    # Upload the icon
    file_input = auth_page.locator('input[name="filepond"]').first
    file_input.set_input_files(test_icon_path)
    auth_page.wait_for_timeout(2000) # Wait for upload
    print(f"[OK] Uploaded icon")
    
    # 5. Submit the form
    submit_button = auth_page.locator('button[type="submit"]').filter(has_text="Create").first
    submit_button.click()
    print("[OK] Clicked Create button")
    
    # Handle possible validation errors
    auth_page.wait_for_timeout(2000)
    if auth_page.locator(".fi-modal-header").filter(has_text="Create social").is_visible():
        print("[WARNING] Creation modal still visible. Retrying submit...")
        submit_button.click()
        auth_page.wait_for_timeout(3000)
    
    # 6. Verify creation
    auth_page.wait_for_timeout(3000)
    
    print("\n[STEP 3] Verifying social creation...")
    search_input = auth_page.locator("input[placeholder*='Search']").first
    search_input.fill(test_title)
    search_input.press("Enter")
    auth_page.wait_for_timeout(2000)
    
    social_row = auth_page.locator("table tr").filter(has_text=test_title).first
    expect(social_row).to_be_visible()
    print(f"[OK] Social '{test_title}' found in the list.")
    
    # 7. Delete the social
    print(f"\n[STEP 4] Deleting the social '{test_title}'...")
    # Scroll right if needed or just find the button
    delete_btn = social_row.locator("button, a").filter(has_text="Delete").first
    expect(delete_btn).to_be_visible()
    delete_btn.click()
    
    # Handle Confirmation Modal
    print("Waiting for confirmation modal...")
    confirm_btn = auth_page.locator(".fi-modal").locator("button").filter(has_text="Confirm").filter(visible=True).first
    expect(confirm_btn).to_be_visible()
    confirm_btn.click()
    
    # 8. Final Verification
    print("\n[STEP 5] Verifying deletion...")
    auth_page.wait_for_timeout(3000)
    
    search_input.fill(test_title)
    search_input.press("Enter")
    auth_page.wait_for_timeout(2000)
    
    # Check for empty state
    empty_state = auth_page.get_by_text("No socials", exact=False).or_(auth_page.get_by_text("No results", exact=False))
    
    if empty_state.count() > 0:
        print("[OK] Empty state visible.")
    else:
        expect(auth_page.locator("table")).not_to_contain_text(test_title)
    
    print(f"[SUCCESS] Social '{test_title}' is definitively gone.")
    
    # Cleanup temp file
    try:
        os.remove(test_icon_path)
    except:
        pass
