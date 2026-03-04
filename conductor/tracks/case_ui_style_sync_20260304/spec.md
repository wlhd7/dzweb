# Specification: Case UI Style Sync (case_ui_style_sync_20260304)

## Overview
Optimize the "Case Study" (经典案例) UI to ensure visual consistency with the rest of the website. This involves moving inline styles to a unified CSS approach and aligning the sidebar with the standard navigation patterns.

## Functional Requirements
- **Sidebar Normalization**:
  - Integrate `nav-top-icon-dashed` SVG icons for all case list items in the sidebar.
  - Implement `<hr>` horizontal dividers between each item in the sidebar list.
  - Standardize padding and margins to match other modules (e.g., Home, Products).
- **Admin Link Styling**:
  - Transform all admin-only buttons (Add, Edit, Delete, Move Up/Down) into hyperlink-style elements.
  - Use `steelblue` for primary actions (Add, Edit) and `red` for destructive actions (Delete).
  - Ensure all admin controls are always visible when the administrator is logged in.
- **CSS Consolidation**:
  - Extract inline styles from `dzweb/templates/case/main.html` and `dzweb/templates/case/display.html`.
  - Introduce reusable CSS classes in `dzweb/static/css/base.css` (e.g., `.link-admin`, `.link-delete`) if they don't already exist.

## Non-Functional Requirements
- **Consistency**: Maintain the "industrial/professional" aesthetic of the dzweb brand.
- **Maintainability**: Ensure code follows the "Snake_case for Python, kebab-case for CSS" naming convention.
- **Internationalization**: All newly added or modified text strings must be wrapped in Flask-Babel's `_()` or `_l()` for multi-language support.

## Acceptance Criteria
- [ ] Sidebar in "Case Study" section is visually indistinguishable from the sidebar in the "Product" or "About Us" sections.
- [ ] All management buttons in the Case section appear as clean, text-based hyperlinks.
- [ ] No significant inline styles remain in the case-related templates.
- [ ] The UI remains fully functional and intuitive for administrators.

## Out of Scope
- Adding new functional features to the "Case Study" module.
- Refactoring the backend API or database schema.
- Modifying parts of the website unrelated to the "Case Study" module.
