import os
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
import time

# Load environment variables
load_dotenv()

def test_add_video_comprehensive(auth_page: Page):
    """
    Comprehensive test to add a video with all required fields filled.
    """
    # 1. Start from dashboard
    auth_page.goto("https://admin.cryptocat.ssd.uz/admin")
    
    # 2. Navigate to Videos tab
    videos_link = auth_page.locator("a.fi-sidebar-item-button").filter(has_text="Videos")
    videos_link.click()
    auth_page.wait_for_url("**/admin/videos**")
    
    # 3. Click create button
    create_button = auth_page.locator("button, a").filter(has_text="Create").or_(
        auth_page.locator("button, a").filter(has_text="New")
    ).first
    create_button.click()
    auth_page.wait_for_timeout(2000)
    
    # 4. Fill in the form
    timestamp = int(time.time())
    test_video_title = f"Test Video {timestamp}"
    
    # Fill the required title field
    title_input = auth_page.locator('#data\\.title')
    expect(title_input).to_be_visible()
    title_input.fill(test_video_title)
    print(f"[OK] Filled title: {test_video_title}")
    
    # 5. Create and upload a dummy video file
    import tempfile
    
    temp_dir = tempfile.gettempdir()
    test_video_path = os.path.join(temp_dir, f"test_video_{timestamp}.mp4")
    
    # Create a minimal valid MP4 file
    mp4_header = bytes([
        0x00, 0x00, 0x00, 0x20, 0x66, 0x74, 0x79, 0x70,
        0x69, 0x73, 0x6F, 0x6D, 0x00, 0x00, 0x02, 0x00,
        0x69, 0x73, 0x6F, 0x6D, 0x69, 0x73, 0x6F, 0x32,
        0x6D, 0x70, 0x34, 0x31, 0x00, 0x00, 0x00, 0x08,
        0x66, 0x72, 0x65, 0x65
    ])
    
    with open(test_video_path, 'wb') as f:
        f.write(mp4_header)
    
    print(f"[OK] Created test video file: {test_video_path}")
    
    # Upload the video file
    file_inputs = auth_page.locator('input[type="file"]').all()
    uploaded = False
    for file_input in file_inputs:
        try:
            file_input.set_input_files(test_video_path)
            print(f"[OK] Uploaded test video file")
            uploaded = True
            auth_page.wait_for_timeout(2000)
            break
        except Exception:
            continue
    
    if not uploaded:
        print("[WARNING] Could not upload video file")
    
    # Check for any validation errors before submitting
    auth_page.wait_for_timeout(500)
    
    # Look for any error messages
    error_messages = auth_page.locator('[class*="error"], [class*="invalid"], .text-danger, [role="alert"]').all()
    visible_errors = []
    for error in error_messages:
        try:
            if error.is_visible():
                error_text = error.inner_text()
                if error_text.strip():
                    visible_errors.append(error_text)
        except:
            continue
    
    if visible_errors:
        print(f"[WARNING] Validation errors found before submit: {visible_errors}")
    
    # Take a screenshot before submitting
    auth_page.screenshot(path="before_submit.png")
    print("Screenshot saved: before_submit.png")
    
    # 5. Submit the form
    create_submit_button = auth_page.locator('button[type="submit"]').filter(has_text="Create").first
    
    # Wait for the upload to complete (button becomes enabled)
    print("Waiting for upload to complete...")
    expect(create_submit_button).to_be_enabled(timeout=30000)
    
    create_submit_button.click()
    print("[OK] Clicked Create button")
    
    # Wait for success and redirect
    auth_page.wait_for_timeout(3000)
    
    # 6. Verify creation
    # Check for success notification (optional, but good to wait for)
    try:
        expect(auth_page.locator('div[role="status"]')).to_contain_text("Created", timeout=5000)
        print(f"[OK] Video '{test_video_title}' was created successfully!")
    except:
        print("[INFO] 'Created' notification not found, proceeding with URL check.")
    
    # Check if we were redirected to the edit page
    import re
    expect(auth_page).to_have_url(re.compile(r".*/admin/videos/\d+/edit"), timeout=10000)
    print(f"[OK] Redirected to edit page for video '{test_video_title}'")
    
    # 7. Delete the video
    print(f"\n[STEP 4] Deleting the video '{test_video_title}'...")
    
    if "/edit" in auth_page.url:
        # Delete from edit page
        delete_btn = auth_page.locator("button").filter(has_text="Delete").first
        expect(delete_btn).to_be_visible()
        delete_btn.click()
    else:
        # Delete from table row
        video_row = auth_page.locator("table tr").filter(has_text=test_video_title).first
        delete_btn = video_row.locator("button, a").filter(has_text="Delete").first
        expect(delete_btn).to_be_visible()
        delete_btn.click()
    
    # Handle Confirmation Modal
    print("Waiting for confirmation modal...")
    confirm_btn = auth_page.locator(".fi-modal, .fi-drawer").locator("button").filter(has_text="Confirm").or_(
        auth_page.locator("button").filter(has_text="Confirm")
    ).filter(visible=True).first
    expect(confirm_btn).to_be_visible()
    confirm_btn.click()
    print("[OK] Confirmed deletion")
    
    # 8. Final Verification
    print("\n[STEP 5] Verifying deletion...")
    auth_page.wait_for_timeout(3000)
    
    # Go back to videos list if we're not there
    if "/admin/videos" not in auth_page.url:
        auth_page.goto("https://admin.cryptocat.ssd.uz/admin/videos")
        
    search_input = auth_page.locator("input[placeholder*='Search']").first
    search_input.fill(test_video_title)
    search_input.press("Enter")
    auth_page.wait_for_timeout(2000)
    
    # Check for empty state or absence
    empty_state = auth_page.get_by_text("No videos", exact=False).or_(auth_page.get_by_text("No results", exact=False))
    
    if empty_state.count() > 0:
        print("[OK] Empty state visible.")
    else:
        expect(auth_page.locator("table")).not_to_contain_text(test_video_title)
    
    print(f"[SUCCESS] Video '{test_video_title}' is definitively gone.")
    
    # Cleanup: remove the temporary test file
    try:
        os.remove(test_video_path)
        print(f"[OK] Cleaned up test video file")
    except:
        pass

