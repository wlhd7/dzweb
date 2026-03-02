# API & Blueprint Architecture (English)

## Blueprint Structure
The application follows the Flask Application Factory pattern with modular blueprints registered in `dzweb/__init__.py`.

### 1. Home (`routes/home.py`)
- `/`: Homepage with company intro and business highlights.
- `/about`: Company history and culture.

### 2. Product (`routes/product.py`)
- `/product`: Product list with category filters.
- `/product/<int:id>/display`: Detailed product view (loads original asset).
- `/product/create` (POST): Admin entry to upload new products (triggers thumbnail generation).
- `/product/<int:id>/delete`: Silent removal of record and physical assets (Original & Thumbnail).

### 3. Human & HR (`routes/human.py`)
- `/human`: Job board.
- `/human/update` (POST): Admin entry to update job positions.

### 4. Admin (`routes/admin.py`)
- `/admin/login`: Simple password-based login using `DZWEB_ADMIN_PASSWORD`.
- `/admin/apps`: Internal tool navigation management.

### 5. Contact (`routes/contact.py`)
- `/contact`: Message board and feedback submission (No location/map).

## External Integrations
### Baidu Active Push (SEO)
- **Endpoint**: `http://data.zz.baidu.com/urls`
- **Logic**: Triggered in `product.py` whenever a new product is created.
- **Payload**: Pushes the URL of the new product for all supported languages (zh, en, ja).
- **Security**: Requires `BAIDU_PUSH_TOKEN` in the environment.

## API Contracts
- **Return Types**: Mix of rendered Jinja2 templates and JSON responses for AJAX/API endpoints.
- **I18n Integration**: Locale is automatically handled by `dzweb/lang.py`.
