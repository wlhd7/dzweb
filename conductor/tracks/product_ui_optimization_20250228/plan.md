# Implementation Plan - product_ui_optimization_20250228

## Phase 1: Sidebar Navigation Update
- [ ] Task: Add "Add New" link to the product sidebar
    - [ ] Write failing tests to verify the presence of the "新增" link for admin users
    - [ ] Modify `dzweb/templates/product/main.html` to insert the "新增" link next to "产品类别" title
    - [ ] Ensure the link only shows when `g.user` is present (Admin)
    - [ ] Verify tests pass

## Phase 2: Form Layout Refactor
- [ ] Task: Adjust label and input alignment in CSS
    - [ ] Modify `dzweb/static/css/product.css` to reduce gap between label and inputs
    - [ ] Adjust `.description-item` to align label to the left-top of textarea
    - [ ] Implement `fit-content` width for the save button
- [ ] Task: Center form container
    - [ ] Update `.product-form` or its parent container style to center the content
- [ ] Task: Apply layout changes to templates
    - [ ] Ensure `product/create.html` and `product/update.html` structure matches the new CSS logic
    - [ ] Verify visually in the browser

## Phase 3: Finalization
- [ ] Task: Regression testing across different screen sizes
- [ ] Task: Conductor - User Manual Verification 'UI Refactor' (Protocol in workflow.md)