# Implementation Plan - remove_app_password_20250228

## Phase 1: Backend Refactor [checkpoint: 847bfb2]
- [x] Task: Remove password-based app addition logic (2421aa9)
    - [x] Write failing tests for app list access (should not require password)
    - [x] Remove `apppassword` related fields or validation logic in `dzweb/routes/user.py`
    - [x] Update `dzweb/db.py` or `schema.sql` if necessary (though we might just ignore the field)
    - [x] Verify tests pass
- [x] Task: Create API/Service to fetch all available apps (a3b1524)
    - [x] Write tests for fetching all apps
    - [x] Implement a function in `dzweb/db.py` to get all entries from `apps` table
    - [x] Verify tests pass
- [x] Task: Conductor - User Manual Verification 'Phase 1: Backend Refactor' (Protocol in workflow.md) (847bfb2)

## Phase 2: Frontend Implementation
- [x] Task: Integrate all-apps list into User Home sidebar (ca2ffc8)
    - [x] Write tests for sidebar rendering with app links
    - [x] Modify `dzweb/templates/user/userhome.html` or the relevant sidebar macro
    - [x] Inject the list of all apps into the template context
    - [x] Verify tests pass
- [x] Task: Remove "Add App" form and password dialogs (8a4059f)
    - [x] Remove the "Add App" button and the corresponding modal/form from the UI
    - [x] Verify tests pass
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Frontend Implementation' (Protocol in workflow.md)

## Phase 3: Cleanup & Finalization
- [ ] Task: Final regression testing on mobile and desktop
- [ ] Task: Remove obsolete code and templates (e.g., `add-app.html` if no longer used)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Cleanup & Finalization' (Protocol in workflow.md)