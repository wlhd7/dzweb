# Implementation Plan: Case Slug Manual Configuration

## Phase 1: Preparation and Backend Cleanup
- [x] Task: Remove `deep_translator` from `dzweb/routes/case.py` and delete `auto_translate`.
- [x] Task: Refactor `api_create_module` to accept manual `slug` from form data.
- [x] Task: Refactor `api_update_module` to accept manual `slug` from form data.
- [x] Task: Verify that `slugify` correctly handles alphanumeric characters and strips others.

## Phase 2: Frontend Enhancement
- [x] Task: Modify `dzweb/templates/case/display.html` to add a visible `slug` input to `add-case-modal`.
- [x] Task: Modify `dzweb/templates/case/display.html` to add a visible `slug` input to `edit-case-title-modal`.
- [x] Task: Update the JavaScript in `dzweb/templates/case/display.html` to capture and send the manually entered slug for both creation and update operations.

## Phase 3: Verification and Testing
- [x] Task: Perform a manual test creating a new case module with a custom slug (e.g., `test-manual-slug`).
- [x] Task: Perform a manual test updating an existing case module's slug.
- [x] Task: Conductor - User Manual Verification 'Case Slug Manual Configuration' (Protocol in workflow.md)
