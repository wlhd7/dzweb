# Resource Maintenance & Hygiene (dzweb)

## 1. Physical Image Cleanup Logic
When a record in the `products` table is removed or its `filename` is updated, the physical file must be deleted from `dzweb/static/uploads/`.

### 1.1 Deletion Sequence
1.  **Identify Files**: Fetch `filename` and identify both original and thumbnail paths.
2.  **Physical Removal**: Use `os.remove()` for both files inside a `try...except` block.
3.  **Database Commit**: Commit the `DELETE` or `UPDATE` after physical file handling.
4.  **UX Strategy**: Success is handled silently (no Flash message) to provide a smoother administrative experience.

## 2. CLI Cleanup Tool (cleanup-images)
A built-in maintenance command reconciles the filesystem with the database.

### 2.1 Logic Workflow
1.  **Reference Scan**: Collect all `filename` values from the `products` table.
2.  **Directory Listing**: Scan both `dzweb/static/uploads/` and `dzweb/static/uploads/thumbs/`.
3.  **Orphan Identification**: Identify files present on disk but absent in the database.
4.  **Batch Deletion**: Automatically remove identified orphan files from both directories.

### 2.2 Execution
```bash
flask cleanup-images
```

## 3. Thumbnail Management
A dedicated CLI command is available to regenerate missing thumbnails for existing products.

```bash
flask generate-thumbs
```

- **Logic**: Iterates through all products and checks if a corresponding thumbnail exists in the `thumbs/` folder. If missing, it generates one using the original image.
- **Safety**: Skips processing if the original image is missing.

