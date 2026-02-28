# Security & Authentication Logic (English)

## Authentication Mechanism
- **Engine**: Flask-Session.
- **Password**: Hashed using `bcrypt`.
- **Login Flow**: Defined in `dzweb/routes/auth.py`.

## Permission Levels
1. **Anonymous**: Can view homepage, products, cases, and recruitment posts.
2. **Authenticated User**: Can access internal navigation and specific tools (apps).
3. **Role-based Controls**:
   - `applist` field in `users` table determines which specific internal apps a user can see/access.
   - Special routes (like `product.create`, `human.update`) check for administrative presence.

## Security Constraints
- **File Uploads**: Product images are restricted to `instance/uploads/`.
- **Secrets**: SECRET_KEY and Mail credentials must remain in `instance/config.py`.
