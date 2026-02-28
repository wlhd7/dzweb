# Implementation Plan - nav_cleanup_20250228

## Phase 1: Navigation Enhancement [checkpoint: be52fbc]
- [x] Task: Add "User Home" link to the global navigation bar (be52fbc)
    - [x] Write tests to verify the presence of the "主页" link for logged-in users
    - [x] Modify `dzweb/templates/base.html` to insert the link between username and logout
    - [x] Verify tests pass

## Phase 2: Feature Cleanup - Set Color [checkpoint: be52fbc]
- [x] Task: Remove "Set User Color" feature (be52fbc)
    - [x] Write failing tests for `/user/set-color` (should return 404)
    - [x] Delete `dzweb/templates/user/set-color.html`
    - [x] Remove `set_color` route and logic from `dzweb/routes/user.py`
    - [x] Remove "设置用户名颜色" from database `apps` table
    - [x] Verify tests pass

## Phase 3: Feature Cleanup - Weekend Overtime [checkpoint: be52fbc]
- [x] Task: Remove "Weekend Overtime" feature (be52fbc)
    - [x] Write failing tests for `/user/weekend-overtime` (should return 404)
    - [x] Delete `dzweb/templates/user/weekend-overtime.html`
    - [x] Remove `weekend_overtime` route, `cleanup_old_data` helper, and related imports from `dzweb/routes/user.py`
    - [x] Remove "周末加班单" from database `apps` table
    - [x] Verify tests pass

## Phase 4: Finalization [checkpoint: be52fbc]
- [x] Task: Regression testing and UI verification (be52fbc)
- [x] Task: Conductor - User Manual Verification 'Finalization' (Protocol in workflow.md) (be52fbc)
