# Cryptocat Video Tests

This document describes the automated tests for the Videos functionality in the Cryptocat admin panel.

## Test Files

### test_add_video.py
Contains three test functions for the Videos tab:

1. **test_navigate_to_videos_tab**
   - Verifies that users can navigate to the Videos tab from the sidebar
   - Checks that the URL changes to include '/videos'

2. **test_add_new_video** ⭐ Main Test
   - Tests the complete flow of adding a new video
   - Creates a dummy MP4 file for upload
   - Fills in the required title field
   - Uploads the video file
   - Submits the form
   - Verifies successful creation by checking the redirect
   - Cleans up the temporary test file

3. **test_videos_list_visible**
   - Verifies that the videos list page displays correctly
   - Checks for either a table/list or an empty state message

## How to Run

### Run all video tests:
```bash
pytest test_add_video.py -v
```

### Run a specific test:
```bash
pytest test_add_video.py::test_add_new_video -v
```

### Run with output visible:
```bash
pytest test_add_video.py -v -s
```

## Test Details

### Form Requirements
The video creation form requires:
- **Title** (required): Text field with ID `data.title`
- **Video File** (required): File upload field
- Optional fields: `data.title_uz` (Uzbek), `data.title_ru` (Russian)

### Test Video File
The test creates a minimal valid MP4 file (36 bytes) with a proper MP4 header. This is sufficient for testing the upload functionality without requiring large video files.

### Success Criteria
The test considers video creation successful if:
1. The form submits without validation errors
2. The page redirects away from the `/create` page
3. The redirect goes to either the videos list or the edit page for the new video

## Diagnostic Tests

### test_explore_video_form.py
A diagnostic test that explores the video creation form structure:
- Lists all input fields with their attributes
- Lists all textarea fields
- Lists all select fields
- Identifies submit buttons
- Takes a screenshot for visual reference

This test is useful for understanding the form structure when debugging or updating tests.

### test_video_comprehensive.py
A comprehensive diagnostic test that:
- Checks for validation errors before and after submission
- Verifies button state (enabled/disabled)
- Takes screenshots at multiple stages
- Provides detailed logging

## Notes

- All tests require valid credentials in the `.env` file
- Tests use Playwright for browser automation
- The dummy video file is automatically cleaned up after each test
- Tests include proper waits for dynamic content to load
