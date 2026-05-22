# Advanced Filters & Delete Action Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Excel-style column filters (Level & Status) and a delete action with physical file removal and confirmation modal.

**Architecture:** 
- **Filters:** Pure JavaScript client-side logic using Bootstrap dropdowns with checkboxes.
- **Delete:** Flask backend route for removing data and files, coupled with a Bootstrap Modal for confirmation.

**Tech Stack:** Python/Flask, Bootstrap 5, JavaScript.

---

### Task 1: Backend Delete Logic

**Files:**
- Modify: `app.py`
- Modify: `logic_engine.py` (Add ID to item if not present)

- [ ] **Step 1: Ensure items in `data_store` have unique IDs**
Update `handle_input` in `app.py` to assign a timestamp-based or incremental ID.
```python
import time
# ...
@app.route('/input', methods=['POST'])
def handle_input():
    # ...
    item = {
        'id': int(time.time() * 1000), # Add unique ID
        'tower': tower,
        # ...
    }
```

- [ ] **Step 2: Add delete route to `app.py`**
```python
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    global data_store
    item_to_delete = next((item for item in data_store if item['id'] == item_id), None)
    
    if item_to_delete:
        # Physical file removal
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], item_to_delete['img'])
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Remove from memory
        data_store = [item for item in data_store if item['id'] != item_id]
        
    return render_template('index.html', items=data_store)
```

- [ ] **Step 3: Commit backend changes**
```bash
git add app.py
git commit -m "feat: add backend logic for data and file deletion"
```

---

### Task 2: Delete UI & Modal

**Files:**
- Modify: `templates/index.html`

- [ ] **Step 1: Add Delete Button to each row**
In the table body, add the red square button with the trash icon.
```html
<td>
    <div class="d-flex align-items-center gap-2">
        <a href="{{ url_for('static', filename='uploads/' + item.img) }}" target="_blank">
            <i class="fas fa-image text-primary"></i>
        </a>
        <button class="btn btn-danger btn-sm rounded-2 shadow-sm" 
                data-bs-toggle="modal" 
                data-bs-target="#deleteModal" 
                onclick="setDeleteTarget('{{ item.id }}')">
            <i class="fas fa-trash"></i>
        </button>
    </div>
</td>
```

- [ ] **Step 2: Add Modal to index.html**
Add the custom styled modal at the end of the file.
```html
<div class="modal fade" id="deleteModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow" style="border-radius: 15px;">
            <div class="modal-body text-center p-4">
                <p class="fs-5 mb-4 fw-bold">Apakah anda yakin ingin menghapus data ini?<br>
                <span class="text-muted fw-normal small">(data akan terhapus secara permanen)</span></p>
                <div class="d-flex justify-content-center gap-3">
                    <form id="deleteForm" method="POST">
                        <button type="submit" class="btn btn-danger px-4 py-2 fw-bold" style="border-radius: 8px;">YA</button>
                    </form>
                    <button class="btn btn-primary px-4 py-2 fw-bold" data-bs-dismiss="modal" style="border-radius: 8px; background-color: #00A2E9;">TIDAK</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function setDeleteTarget(id) {
    document.getElementById('deleteForm').action = '/delete/' + id;
}
</script>
```

- [ ] **Step 3: Commit UI changes**
```bash
git add templates/index.html
git commit -m "feat: add delete button and confirmation modal"
```

---

### Task 3: Advanced Column Filters (Excel-style)

**Files:**
- Modify: `templates/index.html`

- [ ] **Step 1: Update Table Headers with Filter Dropdowns**
Add the filter icons and dropdowns to 'Level Korosifitas' and 'Status' headers.
```html
<th>
    Level Korosifitas 
    <div class="dropdown d-inline ms-1">
        <i class="fas fa-filter text-muted small" style="cursor:pointer" data-bs-toggle="dropdown"></i>
        <div class="dropdown-menu p-3 shadow-sm border-0" style="min-width: 150px; border-radius: 10px;">
            <div class="filter-options-level">
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="C1"> <label>C1</label></div>
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="C2"> <label>C2</label></div>
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="C3"> <label>C3</label></div>
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="C4"> <label>C4</label></div>
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="C5"> <label>C5</label></div>
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="CX"> <label>CX</label></div>
            </div>
        </div>
    </div>
</th>
<th>
    Status 
    <div class="dropdown d-inline ms-1">
        <i class="fas fa-filter text-muted small" style="cursor:pointer" data-bs-toggle="dropdown"></i>
        <div class="dropdown-menu p-3 shadow-sm border-0" style="min-width: 150px; border-radius: 10px;">
            <div class="filter-options-status">
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="Aman"> <label>Aman</label></div>
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="Waspada"> <label>Waspada</label></div>
                <div class="form-check"><input class="form-check-input filter-check" type="checkbox" value="Kritis"> <label>Kritis</label></div>
            </div>
        </div>
    </div>
</th>
```

- [ ] **Step 2: Update JavaScript for multi-criteria filtering**
Refactor the filter script to handle both free-text search and column checkboxes.
```javascript
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('tableSearch');
        const checkboxes = document.querySelectorAll('.filter-check');
        const tableBody = document.querySelector('table tbody');
        const itemCount = document.getElementById('itemCount');

        function filterTable() {
            const query = searchInput.value.toLowerCase();
            const checkedLevels = Array.from(document.querySelectorAll('.filter-options-level .filter-check:checked')).map(c => c.value);
            const checkedStatus = Array.from(document.querySelectorAll('.filter-options-status .filter-check:checked')).map(c => c.value);
            
            const rows = tableBody.querySelectorAll('tr');
            let visibleCount = 0;

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const levelCell = row.cells[5].textContent.trim();
                const statusCell = row.cells[8].textContent.trim();

                const matchesSearch = text.includes(query);
                const matchesLevel = checkedLevels.length === 0 || checkedLevels.includes(levelCell);
                const matchesStatus = checkedStatus.length === 0 || checkedStatus.includes(statusCell);

                if (matchesSearch && matchesLevel && matchesStatus) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            if (itemCount) itemCount.textContent = visibleCount;
        }

        searchInput.addEventListener('keyup', filterTable);
        checkboxes.forEach(cb => cb.addEventListener('change', filterTable));
    });
</script>
```

- [ ] **Step 3: Final check and Commit**
```bash
git add templates/index.html
git commit -m "feat: implement excel-style column filters"
```
