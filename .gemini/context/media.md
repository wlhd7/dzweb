# Media Management & Image Processing (English)

## 1. Storage Strategy
- **Upload Directory**: `dzweb/static/uploads/`
- **Thumbnail Directory**: `dzweb/static/uploads/thumbs/`
- **Volume Config**: `./dzweb/static/uploads:/app/dzweb/static/uploads` (Docker Compose)
- **Asset Access**: Exposed as static assets through Flask.

## 2. Image Processing (`utils/image.py`)
The system uses the `Pillow` library to optimize and resize images upon upload.

### 2.1 Optimization
To balance visual fidelity and loading speed:
- **Optimization**: Enabled during save (`optimize=True`).
- **Quality**: Set to 85 for thumbnails.
- **Format**: Original format (JPG/PNG) is preserved to maintain compatibility.

### 2.2 Thumbnail Generation
To maintain a clean grid and improve page performance:
- **Resizing**: Images are cropped and resized to 400x300px using `ImageOps.fit`.
- **Downsampling**: Uses `Image.Resampling.LANCZOS` for high-quality results.

## 3. Physical Cleanups
- **Strategy**: Synchronous cleanup triggered by DB `UPDATE` or `DELETE` in `routes/product.py`.
- **Integrity**: Both the original image and its corresponding thumbnail are removed simultaneously.
- **CLI Tool**: `flask cleanup-images` provides a way to remove orphan files not referenced in the database.

## 4. Usage in Templates
- **Original**: `<img src="{{ url_for('static', filename='uploads/' + product.filename) }}" alt="...">`
- **Thumbnail**: `<img src="{{ url_for('static', filename='uploads/thumbs/' + product.filename) }}" alt="...">`
- **Best Practice**: Use thumbnails in grid views and original images in detail views.
