# Database Schema Context (English)

## Engine
- **Type**: SQLite
- **Path**: `instance/dzweb.sqlite`

## Entity Relationship Model
1. **users**: Auth and permission base.
   - `id`, `username`, `password` (hashed with bcrypt), `color`, `applist` (comma-separated list of allowed apps).
2. **products**: Catalog items.
   - `id`, `productname`, `brief`, `category` (e.g., automation, robotics), `class` (sub-category), `filename` (linked to static asset).
3. **positions**: HR recruitment info.
   - `id`, `position`, `salary`, `requirement`.
4. **messages**: Customer feedback.
   - `id`, `author_id` (optional user link), `message`, `created`.
5. **apps**: Internal tool directory.
   - `id`, `appname`, `apppassword`, `appurl`.
6. **staffs**: Employee directory.
   - `id`, `name`, `department`, `sub_department`.

## Migration Strategy
- Manual `schema.sql` execution via `dzweb/db.py`'s `init_db` command.
