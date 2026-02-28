# Implementation Plan - admin_panel_refactor_20250228

## Phase 1: Authentication Refactor
- [ ] Task: Transition to Admin-only login
    - [ ] Update `tests/conftest.py` to support `ADMIN_PASSWORD` environment variable for tests
    - [ ] Modify `dzweb/routes/auth.py`:
        - [ ] Remove `register` route and logic
        - [ ] Update `login` route to accept only `password` and verify against `ADMIN_PASSWORD`
        - [ ] Update `load_logged_in_user` to handle admin session without DB user lookup
    - [ ] Update `dzweb/templates/auth/login.html` to remove username field
    - [ ] Delete `dzweb/templates/auth/register.html`
    - [ ] Verify tests pass

## Phase 2: UI & Link Cleanup
- [ ] Task: Remove "Employee Entrance" and update Panel labels
    - [ ] Remove "员工入口" link from `dzweb/templates/home/index.html`
    - [ ] Global search and replace: "个人主页" -> "管理后台" across all templates
    - [ ] Verify tests pass

## Phase 3: Route & Title Migration
- [ ] Task: Rename routes and update specific titles
    - [ ] Update `dzweb/routes/user.py`:
        - [ ] Rename `edit_product_permission` route to `edit-product`
        - [ ] Rename `edit_hire_permission` route to `edit-hire`
    - [ ] Update `dzweb/templates/user/edit-product-permission.html`:
        - [ ] Update title to "编辑产品信息"
    - [ ] Update `dzweb/templates/user/edit-hire-permission.html`:
        - [ ] Update title to "编辑招聘信息"
    - [ ] Verify tests pass

## Phase 4: Finalization
- [ ] Task: Regression testing and documentation sync
- [ ] Task: Conductor - User Manual Verification 'Admin Panel Refactor' (Protocol in workflow.md)