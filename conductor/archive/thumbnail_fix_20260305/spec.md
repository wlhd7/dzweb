# Track Specification: Fix Product Thumbnail Cropping

## Overview
Currently, the system uses `ImageOps.fit` to generate 400x300 thumbnails for products and cases. This method proportionally resizes and *crops* the image to fill the target aspect ratio, causing important visual information at the edges to be lost. The goal of this track is to switch the thumbnail generation logic from "Crop/Fit" to "Contain/Pad" to ensure the entire original image is visible within the 400x300 container, using a white background for any letterboxing/pillarboxing.

## Functional Requirements
1.  **Thumbnail Generation Logic Update**:
    - Modify `dzweb/utils/image.py` to stop using `ImageOps.fit`.
    - Implement a "Contain" strategy: scale the image proportionally so the longest side fits within the target dimensions (400x300) without any cropping.
    - Add padding (letterboxing or pillarboxing) with a **white (#FFFFFF)** background to fill the remaining area of the 400x300 thumbnail.
2.  **Batch Regeneration**:
    - Provide a way to regenerate existing thumbnails using the new logic to ensure visual consistency across the site.
3.  **Global Application**:
    - Ensure the change applies to all modules using `generate_thumbnail`, including Products and Cases (Success Stories).

## Acceptance Criteria
- [ ] Product thumbnails on the homepage are no longer cropped; the full original image is visible.
- [ ] Images with aspect ratios different from 4:3 (400x300) have white padding on the sides or top/bottom.
- [ ] Case study (Success Stories) thumbnails follow the same "no-cropping" rule.
- [ ] Existing thumbnails can be updated to the new format.

## Out of Scope
- Changing the default thumbnail size (400x300).
- Modifying the full-size image or WebP conversion logic (only the thumbnail is affected).
