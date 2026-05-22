# Design Document: Advanced Filters & Delete Action

**Date:** 2026-05-22
**Project:** PLN Tower Corrosion Monitoring Dashboard
**Status:** Approved

## 1. Overview
Adding advanced data management features to the dashboard:
1.  **Excel-style Column Filters:** Allow users to filter the table by 'Status' and 'Level Korosifitas' using a dropdown with checkboxes.
2.  **Delete Action:** Allow users to permanently remove a data entry and its associated image file from the server, with a confirmation modal.

## 2. Technical Specifications

### 2.1. Advanced Column Filters (Excel-style)
- **UI:** A filter icon (FontAwesome `fa-filter`) next to the column headers for "Level Korosifitas" and "Status".
- **Interaction:** Clicking the icon opens a Bootstrap Dropdown menu containing checkboxes for each unique value in that column.
- **Logic:**
    - Uses JavaScript to filter the table rows.
    - If one or more checkboxes are checked, only rows matching any of the checked values will be shown.
    - If no checkboxes are checked, all rows are shown (default).
    - Integrates with the existing free-text search filter.

### 2.2. Delete Action with Confirmation
- **UI:** A red square button with rounded corners and a white trash icon (`fa-trash`) in the 'Gambar' column of each row.
- **Confirmation Modal:**
    - A custom Bootstrap Modal with rounded corners.
    - Text: "Apakah anda yakin ingin menghapus data ini? (data akan terhapus secara permanen)".
    - Buttons: 
        - **YA:** Red background, white text, performs deletion.
        - **TIDAK:** Blue background, white text, closes modal.
- **Backend Logic (Flask):**
    - A new route `/delete/<int:item_id>` or similar.
    - Removes the entry from the in-memory `data_store`.
    - Locates the image file in `static/uploads` and deletes it using `os.remove()`.

## 3. UI/UX Refinements
- **Modal Styling:** `border-radius: 15px` for a modern look.
- **Button Styling:** High contrast colors for action buttons (Success for input, Danger for delete, Info/Primary for navigation).

## 4. Implementation Steps
1.  Update `templates/index.html` with the filter dropdowns and delete buttons.
2.  Implement the JavaScript filtering logic for multiple checkbox selection.
3.  Add the Delete Confirmation Modal to `templates/index.html`.
4.  Add the `/delete` route to `app.py`.
5.  Add file system deletion logic to `app.py`.
