# Implementation Plan - nav_cleanup_20250228

## Phase 1: Navigation Enhancement
- [ ] Task: Add "User Home" link to the global navigation bar
    - [ ] Write tests to verify the presence of the "主页" link for logged-in users
    - [ ] Modify `dzweb/templates/base.html` to insert the link between username and logout
    - [ ] Verify tests pass

## Phase 2: Feature Cleanup - Set Color
- [ ] Task: Remove "Set User Color" feature
    - [ ] Write failing tests for `/user/set-color` (should return 404)
    - [ ] Delete `dzweb/templates/user/set-color.html`
    - [ ] Remove `set_color` route and logic from `dzweb/routes/user.py`
    - [ ] Remove "设置用户名颜色" from database `apps` table
    - [ ] Verify tests pass

## Phase 3: Feature Cleanup - Weekend Overtime
- [ ] Task: Remove "Weekend Overtime" feature
    - [ ] Write failing tests for `/user/weekend-overtime` (should return 404)
    - [ ] Delete `dzweb/templates/user/weekend-overtime.html`
    - [ ] Remove `weekend_overtime` route, `cleanup_old_data` helper, and related imports from `dzweb/routes/user.py`
    - [ ] Remove "周末加班单" from database `apps` table
    - [ ] Verify tests pass

## Phase 4: Finalization
- [ ] Task: Regression testing and UI verification
- [ ] Task: Conductor - User Manual Verification 'Finalization' (Protocol in workflow.md)