# Implementation Plan: Fix Product Thumbnail Cropping

## Phase 1: Preparation and Testing Setup
- [x] Task: Create a failing test case for the new "Contain" thumbnail generation logic. f723e69
    - [x] Create a test image with a high aspect ratio (e.g., 800x200).
    - [x] Assert that the generated thumbnail (400x300) contains the *full* original image and has white padding.
- [x] Task: Verify that current logic fails (it should crop the 800x200 image). f723e69

## Phase 2: Core Logic Update
- [x] Task: Implement "Contain/Pad" logic in `dzweb/utils/image.py`. 2fe6dea
    - [x] Replace `ImageOps.fit` with `ImageOps.pad` or equivalent logic to resize without cropping and add white background.
    - [x] Ensure the high-quality LANCZOS resampling is preserved.
- [x] Task: Verify that the failing test case now passes. 2fe6dea

## Phase 3: CLI Command Enhancement
- [ ] Task: Update the `generate-thumbs` CLI command in `dzweb/routes/product.py` to support a `--force` flag.
    - [ ] Add the `--force` option to the command.
    - [ ] If `--force` is used, overwrite existing thumbnails even if they already exist.
- [ ] Task: Verify the `--force` flag works via manual test or automated test.

## Phase 4: Validation and Verification
- [ ] Task: Run all existing image-related tests to ensure no regressions.
- [ ] Task: Conductor - User Manual Verification 'Thumbnail Display' (Protocol in workflow.md)
