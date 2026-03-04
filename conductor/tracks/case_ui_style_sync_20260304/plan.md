# Implementation Plan: Case UI Style Sync (case_ui_style_sync_20260304)

## Phase 1: Research & Preparation [checkpoint: bea38d5]
- [x] Task: Audit all case templates (`main.html`, `display.html`) for inline styles and admin controls. 07f62ba
- [x] Task: Verify the exact CSS properties for `nav-top-icon-dashed` and `steelblue link` in `base.css`. 07f62ba
- [x] Task: Conductor - User Manual Verification 'Phase 1: Research & Preparation' (Protocol in workflow.md) bea38d5

## Phase 2: CSS Standardization
- [x] Task: Add `.link-admin` and `.link-delete` utility classes to `dzweb/static/css/base.css` to handle text-based management actions. 3e6d502
- [x] Task: Ensure `.nav-top-icon-dashed` is consistently defined for use in case list sidebars. 3e6d502
- [ ] Task: Conductor - User Manual Verification 'Phase 2: CSS Standardization' (Protocol in workflow.md)

## Phase 3: Sidebar Normalization (TDD)
- [ ] Task: Create unit tests to verify the sidebar structure in case templates (presence of icons and dividers).
- [ ] Task: Update `dzweb/templates/case/main.html` sidebar list to match the product list pattern (using icons and `<hr>`).
- [ ] Task: Update `dzweb/templates/case/display.html` sidebar list for consistency.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Sidebar Normalization (TDD)' (Protocol in workflow.md)

## Phase 4: Admin Controls Refactor (TDD)
- [ ] Task: Create unit tests for admin control visibility and link-style rendering.
- [ ] Task: Refactor "Add Case" button and modal buttons in `main.html` to use link-style CSS classes.
- [ ] Task: Refactor content management buttons (Edit, Move Up/Down, Delete) in `display.html` to be text-link based.
- [ ] Task: Clean up all remaining inline styles in case templates.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Admin Controls Refactor (TDD)' (Protocol in workflow.md)

## Phase 5: Verification & Checkpoint
- [ ] Task: Run full test suite with coverage report.
- [ ] Task: Perform manual verification on mobile and desktop viewports.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Verification & Checkpoint' (Protocol in workflow.md)
