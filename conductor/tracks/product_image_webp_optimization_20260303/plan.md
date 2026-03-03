# Implementation Plan - Product Display Page WebP Image Optimization

## Phase 1: Preparation & Infrastructure [checkpoint: 1ca477d]
- [x] Task: Create utility for WebP conversion in `dzweb/utils/image.py` fb2ec83
    - [x] Implement `convert_to_webp(source_path, quality=80)` using Pillow.
    - [x] Ensure it returns the path to the new WebP file.
- [x] Task: Implement Flask CLI command `flask convert-webp` in `dzweb/__init__.py` (or integrated via blueprints). fb2ec83
    - [x] Command should iterate through all full-size images in `UPLOAD_FOLDER`.
    - [x] Generate WebP versions if they don't already exist.
- [x] Task: Write unit tests for the WebP utility and CLI command. fb2ec83
- [x] Task: Conductor - User Manual Verification 'Phase 1: Preparation & Infrastructure' (Protocol in workflow.md) fb2ec83

## Phase 2: Backend Integration [checkpoint: 779b962]
- [x] Task: Update `dzweb/routes/admin.py` (or corresponding service) upload logic. 36d80e4
    - [x] Trigger WebP conversion immediately after a successful product image upload.
- [x] Task: Update resource cleanup logic in `dzweb/routes/admin.py`. 36d80e4
    - [x] Ensure WebP files are physically deleted when the original image is deleted or updated (Sync Deletion/Update Protocol).
- [x] Task: Write tests for upload/delete hooks to verify WebP file synchronization. 36d80e4
- [x] Task: Conductor - User Manual Verification 'Phase 2: Backend Integration' (Protocol in workflow.md) 36d80e4

## Phase 3: Frontend Implementation [checkpoint: 64e0089]
- [x] Task: Modify `dzweb/templates/product/display.html`. d83c6ba
    - [x] Replace standard `<img>` with the HTML5 `<picture>` tag.
    - [x] Add `<source srcset="..." type="image/webp">` pointing to the WebP version.
    - [x] Ensure the fallback `<img>` still points to the original JPG/PNG.
- [x] Task: Verify that the change only affects the individual product display page and not the home/category thumbnails. d83c6ba
- [x] Task: Write integration tests for the product display page to verify `<picture>` and `<source>` tags are rendered correctly. d83c6ba
- [x] Task: Conductor - User Manual Verification 'Phase 3: Frontend Implementation' (Protocol in workflow.md) d83c6ba

## Phase 4: Final Processing & Audit
- [~] Task: Execute the batch conversion: `flask convert-webp`.
- [ ] Task: Perform a final audit of the product display pages to confirm WebP is being served (via DevTools/Network tab).
- [ ] Task: Verify the full lifecycle: Upload a product -> Check WebP exists -> Display page shows WebP -> Delete product -> Both files are removed.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Processing & Audit' (Protocol in workflow.md)
