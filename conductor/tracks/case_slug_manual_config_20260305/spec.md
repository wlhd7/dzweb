# Specification: Case Slug Manual Configuration & Google Translate Removal

## 1. Overview
Remove the dependency on `deep_translator` (Google Translate) for generating case module slugs. Instead, allow administrators to manually specify the `slug` (URL alias) when creating or updating a "Classic Case" (经典案例) module.

## 2. Functional Requirements

### 2.1 Backend (Python/Flask)
- **Remove Dependency**: Uninstall/Remove `deep_translator` usage in `dzweb/routes/case.py`.
- **Remove Function**: Delete the `auto_translate` helper function.
- **Update Routes**:
    - `api_create_module`: Accept an optional `slug` from the POST form. If missing, use `slugify(title_zh)`.
    - `api_update_module`: Accept a new `slug` from the POST form. Update the database record with the new slug.
- **Slug Validation**: Ensure the provided slug is URL-friendly (alphanumeric and dashes) and unique.

### 2.2 Frontend (HTML/JS)
- **UI Update**:
    - Add a visible `slug` input field in the "Add Case Module" modal.
    - Add a visible `slug` input field in the "Edit Case Title" modal.
- **JS Logic**:
    - Update form submission scripts to include the value of the new `slug` input field.
    - Implement client-side validation for slug format (e.g., regex `^[a-z0-9-]+$`).

## 3. Acceptance Criteria
- Administrators can successfully create a new case module by providing a Chinese title and a custom URL slug.
- The creation process must not make any external network requests (specifically to Google Translate).
- Existing cases remain accessible via their current slugs.
- Updating a case title and slug correctly updates the URL and redirects to the new location.

## 4. Out of Scope
- Automatic slug generation using other third-party translation services.
- Bulk renaming of existing slugs.
