# Implementation Plan - remove_app_password_20250228

## Phase 1: Backend Refactor
- [ ] Task: Remove password-based app addition logic
    - [ ] Write failing tests for app list access (should not require password)
    - [ ] Remove `apppassword` related fields or validation logic in `dzweb/routes/user.py`
    - [ ] Update `dzweb/db.py` or `schema.sql` if necessary (though we might just ignore the field)
    - [ ] Verify tests pass
- [ ] Task: Create API/Service to fetch all available apps
    - [ ] Write tests for fetching all apps
    - [ ] Implement a function in `dzweb/db.py` to get all entries from `apps` table
    - [ ] Verify tests pass
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Backend Refactor' (Protocol in workflow.md)

## Phase 2: Frontend Implementation
- [ ] Task: Integrate all-apps list into User Home sidebar
    - [ ] Write tests for sidebar rendering with app links
    - [ ] Modify `dzweb/templates/user/userhome.html` or the relevant sidebar macro
    - [ ] Inject the list of all apps into the template context
    - [ ] Verify tests pass
- [ ] Task: Remove "Add App" form and password dialogs
    - [ ] Remove the "Add App" button and the corresponding modal/form from the UI
    - [ ] Verify tests pass
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Frontend Implementation' (Protocol in workflow.md)

## Phase 3: Cleanup & Finalization
- [ ] Task: Final regression testing on mobile and desktop
- [ ] Task: Remove obsolete code and templates (e.g., `add-app.html` if no longer used)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Cleanup & Finalization' (Protocol in workflow.md)