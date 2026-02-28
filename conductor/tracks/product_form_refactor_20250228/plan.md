# Implementation Plan - product_form_refactor_20250228

## Phase 1: API & Backend Support
- [ ] Task: Create API endpoint for dynamic category mapping
    - [ ] Write failing test for `/product/api/subcategories/<category>`
    - [ ] Implement a function in `dzweb/routes/product.py` to return subcategories as JSON
    - [ ] Verify tests pass

## Phase 2: Frontend Logic & Interaction
- [ ] Task: Implement category-subcategory linkage in JavaScript
    - [ ] Add event listener to the "产品分类" dropdown in `product/create.html`
    - [ ] Implement fetch logic to call the new API and update the "子类别" dropdown
    - [ ] Add logic to disable the dropdown if no subcategories are returned
    - [ ] Verify functionality manually in the browser

## Phase 3: UI Layout & Styling
- [ ] Task: Refactor form styles for spacing and label alignment
    - [ ] Modify CSS (likely `static/css/product.css` or similar) to add gap/margin to form items
    - [ ] Adjust "产品描述" label positioning to be above the textarea
    - [ ] Verify UI on both desktop and mobile
- [ ] Task: Conductor - User Manual Verification 'UI Refactor' (Protocol in workflow.md)