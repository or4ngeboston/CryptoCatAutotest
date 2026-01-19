import os
import time
import tempfile
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# Load environment variables
load_dotenv()

def test_news_comprehensive(auth_page: Page):
    """
    Comprehensive test to create news and then delete it.
    """
    # 1. Start from dashboard
    auth_page.goto("https://admin.cryptocat.ssd.uz/admin")
    
    # 2. Navigate to News tab
    print("\n[STEP 1] Navigating to News...")
    news_link = auth_page.locator("a.fi-sidebar-item-button").filter(has_text="News")
    news_link.click()
    auth_page.wait_for_url("**/admin/news**")
    
    # 3. Click New news button
    print("[STEP 2] Creating new news...")
    create_button = auth_page.locator("button, a").filter(has_text="New news").first
    create_button.click()
    
    # 4. Fill in the form
    timestamp = int(time.time())
    test_title = f"Test News {timestamp}"
    test_body = f"This is a test news body created at {timestamp}."
    
    # Title fields
    auth_page.locator('#mountedActionsData\\.0\\.title').fill(test_title)
    auth_page.locator('#mountedActionsData\\.0\\.title_uz').fill(f"{test_title} UZ")
    auth_page.locator('#mountedActionsData\\.0\\.title_ru').fill(f"{test_title} RU")
    print(f"[OK] Filled titles: {test_title}")
    
    # Image upload
    temp_dir = tempfile.gettempdir()
    test_image_path = os.path.join(temp_dir, f"test_news_{timestamp}.png")
    
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
    with open(test_image_path, 'wb') as f:
        f.write(png_header)
    
    print(f"[OK] Created test image: {test_image_path}")
    
    # Upload the image (Filament uses Filepond)
    file_input = auth_page.locator('input[name="filepond"]').first
    file_input.set_input_files(test_image_path)
    auth_page.wait_for_timeout(2000) # Wait for upload
    print(f"[OK] Uploaded image")
    
    # Body fields (Rich Text Editor / ProseMirror)
    # Target all three required body fields
    body_editors = auth_page.locator('.tiptap.ProseMirror').all()
    
    # We expect at least 3 editors (Body, Body uz, Body ru)
    if len(body_editors) >= 3:
        for idx, editor in enumerate(body_editors):
            lang_suffix = ["", " UZ", " RU"][idx]
            editor.click()
            auth_page.wait_for_timeout(500)
            editor.press_sequentially(f"{test_body}{lang_suffix}", delay=50)
            auth_page.wait_for_timeout(500)
            # Final click to ensure focus and blur events trigger
            editor.click()
        print(f"[OK] Filled all body content editors")
    else:
        print(f"[WARNING] Found only {len(body_editors)} body editors")
    
    # 5. Submit the form
    submit_button = auth_page.locator('button[type="submit"]').filter(has_text="Create").first
    submit_button.click()
    print("[OK] Clicked Create button")
    
    # Handle possible validation errors (e.g. "body is required" if sync failed)
    auth_page.wait_for_timeout(2000)
    if auth_page.locator(".fi-modal-header").filter(has_text="Create news").is_visible():
        print("[WARNING] Creation modal still visible. Retrying submit...")
        submit_button.click()
        auth_page.wait_for_timeout(3000)
    
    # 6. Verify creation
    auth_page.wait_for_timeout(3000)
    
    print("\n[STEP 3] Verifying news creation...")
    search_input = auth_page.locator("input[placeholder*='Search']").first
    search_input.fill(test_title)
    search_input.press("Enter")
    auth_page.wait_for_timeout(2000)
    
    news_row = auth_page.locator("table.fi-ta-table tr").filter(has_text=test_title).first
    expect(news_row).to_be_visible()
    print(f"[OK] News '{test_title}' found in the list.")
    
    # 7. Delete the news
    print(f"\n[STEP 4] Deleting the news '{test_title}'...")
    delete_btn = news_row.locator("button, a").filter(has_text="Delete").first
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
    empty_state = auth_page.get_by_text("No news", exact=False).or_(auth_page.get_by_text("No results", exact=False))
    
    if empty_state.count() > 0:
        print("[OK] Empty state visible.")
    else:
        expect(auth_page.locator("table.fi-ta-table")).not_to_contain_text(test_title)
    
    print(f"[SUCCESS] News '{test_title}' is definitively gone.")
    
    # Cleanup temp file
    try:
        os.remove(test_image_path)
    except:
        pass
