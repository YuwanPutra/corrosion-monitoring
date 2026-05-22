# Table Filter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a real-time free-text search filter for the dashboard's results table.

**Architecture:** Client-side filtering using JavaScript. A search input field will listen for `keyup` events and toggle the visibility of table rows based on whether they contain the search query.

**Tech Stack:** HTML5, CSS3, JavaScript, FontAwesome.

---

### Task 1: UI Implementation & Styling

**Files:**
- Modify: `templates/index.html`
- Modify: `static/css/style.css`

- [ ] **Step 1: Add CSS for the search box**
```css
.search-container { position: relative; max-width: 400px; }
.search-container i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #aaa; }
.search-input { padding-left: 35px; border-radius: 20px; border: 1px solid #ddd; }
.search-input:focus { border-color: #00A2E9; box-shadow: 0 0 0 0.2rem rgba(0, 162, 233, 0.25); }
```

- [ ] **Step 2: Add Search Box to index.html**
Modify the table card header to include the search input.
```html
<div class="card p-4 shadow-sm border-0 rounded-3">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <span class="text-muted">Showing <span id="itemCount">{{ items|length }}</span> Item(s).</span>
        <div class="search-container">
            <i class="fas fa-search"></i>
            <input type="text" id="tableSearch" class="form-control search-input" placeholder="Cari data (Tower, Aksesoris, Status...)...">
        </div>
    </div>
    <!-- ... table code ... -->
```

- [ ] **Step 3: Commit UI changes**
```bash
git add static/css/style.css templates/index.html
git commit -m "feat: add search box UI for table filter"
```

---

### Task 2: JavaScript Filtering Logic

**Files:**
- Modify: `templates/index.html`

- [ ] **Step 1: Add filtering script**
Add the script at the bottom of the `content` block or in a script block.
```javascript
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('tableSearch');
        const tableBody = document.querySelector('table tbody');
        const itemCount = document.getElementById('itemCount');

        if (searchInput && tableBody) {
            searchInput.addEventListener('keyup', function() {
                const query = this.value.toLowerCase();
                const rows = tableBody.querySelectorAll('tr');
                let visibleCount = 0;

                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(query)) {
                        row.style.display = '';
                        visibleCount++;
                    } else {
                        row.style.display = 'none';
                    }
                });

                if (itemCount) {
                    itemCount.textContent = visibleCount;
                }
            });
        }
    });
</script>
```

- [ ] **Step 2: Verify and Commit**
Test the filter in the browser.
```bash
git add templates/index.html
git commit -m "feat: implement real-time table filtering logic"
```
