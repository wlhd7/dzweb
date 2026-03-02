# Resource Maintenance & Hygiene (dzweb)

## 1. Physical Image Cleanup Logic
When a record in the `products` table is removed or its `filename` is updated, the physical file must be deleted from `instance/uploads/`.

### 1.1 Deletion Sequence
1.  **Identify File**: Fetch `filename` from the database using record `id`.
2.  **Path Resolution**: Map to `app.instance_path + '/uploads/' + filename`.
3.  **Physical Removal**: Use `os.remove(file_path)` inside a `try...except` block.
4.  **Database Commit**: Only commit the database `DELETE` or `UPDATE` after successful or non-blocking physical file handling.

## 2. CLI Cleanup Tool (cleanup-images)
A built-in maintenance command is available to reconcile the filesystem with the database.

### 2.1 Logic Workflow
1.  **Reference Scan**: Collect all unique `filename` values from the `products` table.
2.  **Directory Listing**: List all files in `instance/uploads/`.
3.  **Orphan Identification**: Identify files present on disk but absent in the referenced filename set.
4.  **Batch Deletion**: Automatically remove identified orphan files.

### 2.2 Execution
```bash
flask cleanup-images
```

## 3. Error Handling
- **Missing Files**: If `os.remove()` fails because the file is already gone, log a warning and proceed with database deletion.
- **Permission Errors**: Log an error and notify the admin (via flash message). Do NOT delete the database record if physical cleanup is mandatory and fails.
