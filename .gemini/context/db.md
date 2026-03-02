# Database Schema Context (English)

## Engine
- **Type**: SQLite
- **Path**: `instance/dzweb.sqlite`

## Entity Relationship Model
1. **users**: Legacy auth table (currently minimized in favor of environment-based admin).
   - `id`, `username`, `password`, `color`, `applist`.
2. **products**: Catalog items.
   - `id`, `productname`, `brief`, `category`, `filename` (UUID-based), `class` (Sub-category ID), `created`.
3. **positions**: HR recruitment info.
   - `id`, `position`, `salary`, `requirement`, `created`.
4. **messages**: Customer feedback.
   - `id`, `author_id` (optional), `message`, `created`.
5. **apps**: Internal tool directory.
   - `id`, `appname`, `appurl`.
6. **staffs**: Employee directory.
   - `id`, `name`, `department`, `sub_department`.

## Specific Field Logic
### Product `class`
- Used to group products within a main category (e.g., `engine`, `transmission` under `automation`).
- Mapping is defined in `dzweb/routes/product.py` (`SUBCATEGORIES` dictionary).

## Migration & Initialization
- **Init**: Schema is initialized via `dzweb/schema.sql`.
- **Command**: `flask init-db` resets the database to the schema.
- **Persistence**: Managed through Docker volumes (`./instance`).
