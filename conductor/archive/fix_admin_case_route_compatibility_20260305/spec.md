# Specification: Admin Case Route Compatibility Fix

## 1. Overview
The server environment is reporting a `werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'admin.edit_case'`. This is because some database records in the `apps` table point to `admin.edit_case`, but this route has been replaced or moved to `case.main`.

## 2. Functional Requirements
- **Backend (Python/Flask)**:
    - Add a new route `admin.edit_case` to `dzweb/routes/admin.py`.
    - This route should simply redirect the user to `case.main`.
    - This ensures that even if the database contains the old endpoint name, the application will not crash and will redirect the user to the correct case management page.

## 3. Acceptance Criteria
- Accessing `admin.edit_case` via `url_for` in any template or python file no longer raises a `BuildError`.
- The `admin.edit_case` route correctly redirects to `case.main`.
- The admin dashboard correctly loads all app links without error.

## 4. Out of Scope
- Migrating all existing database records to use `case.main` (though this is recommended later).
