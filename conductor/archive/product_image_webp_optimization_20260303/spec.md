# Track Specification: Product Display Page WebP Image Optimization

## Overview
This track focuses on improving the performance of the individual **product display page** (e.g., `product/62/display`) by serving high-resolution images in WebP format (80% quality). The optimization will focus exclusively on the primary "full-size" images shown on the display page, while maintaining original formats as fallbacks for older browsers.

## Functional Requirements
1. **Batch Conversion (CLI)**: Implement a Flask CLI command (`flask convert-webp`) to generate WebP versions for all existing full-resolution product images in `dzweb/static/uploads/`.
2. **Upload Hook**: Modify the image upload logic (in `dzweb/utils/image.py` or `dzweb/routes/admin.py`) to automatically generate a WebP version (80% quality) whenever a new product image is uploaded.
3. **Progressive Rendering**: Update the **product display template** (`dzweb/templates/product/display.html`) to use the HTML5 `<picture>` tag, serving WebP by default and falling back to the original JPG/PNG format.
4. **Maintenance Sync**: Ensure the "Resource Integrity Protocol" (from `GEMINI.md`) is maintained: deleting a product or updating an image must also remove/replace the corresponding WebP file.

## Non-Functional Requirements
- **Quality**: Target 80% WebP quality for an optimal balance between visual fidelity and file size reduction.
- **Compatibility**: Maintain full support for older browsers using progressive enhancement.
- **Performance**: Significant reduction in the payload size of the product display page's primary images.

## Acceptance Criteria
- [ ] A CLI command `flask convert-webp` successfully generates WebP versions for all existing full-size uploads.
- [ ] New product images uploaded via the admin panel have a corresponding WebP file in the uploads folder.
- [ ] The **product display page** (and ONLY the display page) serves WebP to modern browsers and original formats to others.
- [ ] Deleting a product image removes both the original and the WebP file.

## Out of Scope
- **Thumbnails**: Optimization of the 400x300 thumbnails used on the home page and product category lists is EXPLICITLY out of scope for this track.
- **Other Pages**: Home page, service page, and case study page images are not affected by this change.
