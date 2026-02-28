# Implementation Plan - admin_panel_refactor_20250228

## Phase 1: Authentication Refactor
- [x] Task: Transition to Admin-only login (633f8f0)
    - [x] Update `tests/conftest.py` to support `ADMIN_PASSWORD` environment variable for tests
    - [x] Modify `dzweb/routes/auth.py`:
        - [x] Remove `register` route and logic
        - [x] Update `login` route to accept only `password` and verify against `ADMIN_PASSWORD`
        - [x] Update `load_logged_in_user` to handle admin session without DB user lookup
    - [x] Update `dzweb/templates/auth/login.html` to remove username field
    - [x] Delete `dzweb/templates/auth/register.html`
    - [x] Verify tests pass

## Phase 2: UI & Link Cleanup
- [x] Task: Remove "Employee Entrance" and update Panel labels (4e625fa)
    - [x] Remove "员工入口" link from `dzweb/templates/home/index.html`
    - [x] Global search and replace: "个人主页" -> "管理后台" across all templates
    - [x] Verify tests pass

## Phase 3: Route & Title Migration
- [x] Task: Rename routes and update specific titles (d9ea8db)
    - [x] Update `dzweb/routes/user.py`:
        - [x] Rename `edit_product_permission` route to `edit-product`
        - [x] Rename `edit_hire_permission` route to `edit-hire`
    - [x] Update `dzweb/templates/user/edit-product-permission.html`:
        - [x] Update title to "编辑产品信息"
    - [x] Update `dzweb/templates/user/edit-hire-permission.html`:
        - [x] Update title to "编辑招聘信息"
    - [x] Verify tests pass

## Phase 4: Finalization
- [ ] Task: Regression testing and documentation sync
- [ ] Task: Conductor - User Manual Verification 'Admin Panel Refactor' (Protocol in workflow.md)