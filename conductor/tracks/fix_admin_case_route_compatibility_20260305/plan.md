# Implementation Plan: Admin Case Route Compatibility Fix

## Phase 1: Implementation
- [ ] Task: Add `admin.edit_case` route to `dzweb/routes/admin.py` that redirects to `case.main`.
- [ ] Task: Verify the new route existence in python.

## Phase 2: Verification
- [ ] Task: Create a unit test that mocks an app list with `admin.edit_case` and ensures the admin page renders correctly.
- [ ] Task: Conductor - User Manual Verification 'Admin Case Route Compatibility' (Protocol in workflow.md)
