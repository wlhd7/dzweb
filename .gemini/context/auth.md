# Security & Authentication Logic (English)

## Authentication Mechanism
The system uses a simplified, environment-driven administrator authentication flow.

### 1. Global Admin Account
- **Engine**: Flask-Session.
- **Credential**: `DZWEB_ADMIN_PASSWORD` (read from environment/docker-compose).
- **Session Key**: `is_admin: True` is stored in the session upon successful login.

### 2. Login Flow (`routes/admin.py`)
- **Route**: `/admin/login`
- **Validation**: Direct string comparison with the environment variable (bcrypt is NOT used for this administrative account).
- **Fallback**: If `DZWEB_ADMIN_PASSWORD` is missing, the system warns the user and prevents login.

## Permission Control
### Admin-Only Routes
Protected via the `@login_required` decorator in `dzweb/routes/admin.py`.
- **Administrative Actions**: Creating/Updating/Deleting products and recruitment positions.
- **Navigation Management**: Managing internal apps links.

### Anonymous Access
- Viewing public-facing pages: Home, About, Product Lists, Job Board, Contact.

## Security Constraints
- **Session Isolation**: `session.clear()` is called during login and logout.
- **Environment Safety**: Sensitive credentials like `DZWEB_ADMIN_PASSWORD` and `BAIDU_PUSH_TOKEN` are managed outside the source code.
- **Input Sanitization**: Strings like `productname` and `brief` are stripped before DB insertion.
