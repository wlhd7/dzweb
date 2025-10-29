## dzweb — quick orientation for AI coding agents

This repo is a small Flask website (app factory pattern). Below are the most important facts and concrete examples to help you be productive immediately.

- App entry & factory
  - The Flask factory is `create_app` in `dzweb/__init__.py`. It registers blueprints from `dzweb/routes` (the `bps` list) and initializes logging, DB, mail, and i18n.
  - Instance-specific config lives under the `instance/` folder (the app loads `instance/config.py` if present). The SQLite DB file is `instance/dzweb.sqlite` by default.

- Blueprints & routing
  - Blueprints live in `dzweb/routes/*.py` and each module exposes `bp` (e.g. `auth.bp`, `user.bp`). See `dzweb/routes/__init__.py` for how they are registered.
  - The home page query is done in `dzweb/routes/__init__.py` (uses `get_db()` to fetch recent products).

- Database
  - Database helpers are in `dzweb/db.py`. Use `get_db()` to get a connection and rely on `app.teardown_appcontext` to close it. `init-db` CLI command runs `schema.sql`.
  - SQL is used directly (raw queries + `sqlite3.Row` row factory). Example: users are fetched with `SELECT * FROM users WHERE id = ?`.
  - WARNING: some routes (notably `user.weekend_overtime`) modify schema at runtime using `ALTER TABLE` to add date-named columns and drop old columns. Treat DB schema changes carefully — prefer backing up `instance/dzweb.sqlite` before testing changes.

- Authentication & sessions
  - Auth lives in `dzweb/routes/auth.py`. Passwords use `bcrypt` (`bcrypt.hashpw` / `bcrypt.checkpw`) and user id is stored in `session['user_id']`. The `login_required` decorator is provided here and used across routes.

- Email & logging
  - Mail helper: `dzweb/mail.py`. Uses Flask-Mail. Config keys of interest: `MAIL_SERVER`, `MAIL_DEFAULT_SENDER`, `MAIL_ADMINS` or `MAIL_ADMIN` (code checks both patterns).
  - Logging setup is in `dzweb/logging.py`. It writes to `instance/logs/weekend_overtime.log` using a RotatingFileHandler with `maxBytes=1024` and `backupCount=1`.

- Internationalization
  - Translations exist under `translations/` (e.g. `translations/en/LC_MESSAGES/messages.po`). The app initializes Babel via `dzweb/lang.py` (callable from `create_app`). Note: code sets `BABEL_DEFAUTL_LOCALE` in `create_app` — that's likely a typo (should be `BABEL_DEFAULT_LOCALE`).

- Static & templates
  - Templates are in `templates/` and static assets in `static/`. Templates use Jinja2 and are referenced directly by blueprint view functions (e.g., `render_template('user/add-app.html')`).

- Dependencies & packaging
  - See `pyproject.toml` and `requirements.txt`. Key runtime libs: Flask, flask-babel, flask-mail, bcrypt. There are editable installs listed in `requirements.txt` (local `-e /var/www/dzweb` and a git subpackage `weekend_overtime`).

- Dev / runtime commands (concrete)
  - Initialize DB (from repo root):
    export FLASK_APP='dzweb:create_app'
    flask init-db
  - Run dev server:
    flask --app 'dzweb:create_app' --debug run
  - Run with Gunicorn (production example):
    gunicorn 'dzweb:create_app()' -w 4 -b 0.0.0.0:8000

- Project-specific patterns and gotchas
  - Raw SQL everywhere: prefer `get_db()` + parameterized queries (the code uses `?` placeholders). When editing queries, keep the original parameter style.
  - Global request context: many views rely on `g.user`, `g.applist`, and pre-request hooks (see `auth.load_logged_in_user` and `user.load_added_apps`). Ensure any refactor preserves those side-effects.
  - Dynamic schema: `user.weekend_overtime` adds/drops date-named columns at runtime. Avoid naive schema refactors; tests or local DB copies are required before changing that logic.
  - Small log rotation: `maxBytes=1024` — logs fill quickly in development. Check `instance/logs/` when debugging.
  - Typos in config keys: `BABEL_DEFAUTL_LOCALE` looks misspelled in `dzweb/__init__.py` — search for `DEFAUTL` if changing locale behavior.

- Files to open first when making changes
  - `dzweb/__init__.py` (app factory)
  - `dzweb/db.py` (DB helpers & CLI)
  - `dzweb/routes/*.py` (business logic, routing patterns)
  - `dzweb/mail.py` and `dzweb/logging.py` (integration points)
  - `schema.sql` (DB schema)

If anything here is unclear or you want more detail (examples of common edits, tests to add, or safe DB migration steps), tell me which area to expand and I'll iterate.
