# Design Document: PLN Tower Corrosion Monitoring Dashboard

**Date:** 2026-05-22
**Project:** Internal Enterprise Dashboard for UIP3BKAL
**Status:** Approved

## 1. Overview
A web-based internal dashboard for monitoring and analyzing corrosion on power tower accessories using Deep Learning (AI). The system allows users to input tower data, upload images, and automatically receive corrosion percentage, life estimation (ISO 9223), status, and recommended actions.

## 2. Technical Stack
- **Backend:** Python 3.x with Flask
- **AI/ML:** TensorFlow / Keras (MobileNetV2 architecture for lightweight inference)
- **Frontend:** HTML5, CSS3, Bootstrap 5 (Enterprise Style), FontAwesome
- **Data Handling:** Local storage/session (for prototype) or SQLite (for persistence)
- **Calculation Standards:** ISO 9223:2012 for atmospheric corrosion rates.

## 3. UI/UX Design
### 3.1. Navigation Bar (Header)
- Solid Light Blue background.
- Left: Hamburger menu icon, PLN Logo.
- Right: Badges for "UIP3BKAL" and "CONFIG".

### 3.2. Input Section (Upper Card)
- 6-column grid layout:
  1. Tower Number (Text)
  2. Circuit Info (Text)
  3. Accessories (Text)
  4. Inspection Date (Date Picker)
  5. Corrosivity Level (Dropdown: C1, C2, C3, C4, C5, CX)
  6. Accessory Photo (File Upload: .jpg, .jpeg, .png)
- Action: "INPUT DATA" button (Green, Centered).

### 3.4. Table Filter
- A free-text search box placed at the top-right of the results table.
- Real-time client-side filtering using JavaScript.
- Searches across all visible columns (Tower Number, Accessory, Status, etc.).

## 4. Logical Engine
### 4.1. Deep Learning (Corrosion Detection)
- **Model:** Pre-trained MobileNetV2 fine-tuned for corrosion detection OR Color Segmentation in HSV space for percentage calculation.
- **Logic:** Calculate the ratio of "corroded area pixels" to "total accessory area pixels".

### 4.2. Life Estimation (ISO 9223:2012)
- Based on first-year corrosion rates (r_corr) for carbon steel:
  - C1: < 1.3 µm/y
  - C2: 1.3 - 25 µm/y
  - C3: 25 - 50 µm/y
  - C4: 50 - 80 µm/y
  - C5: 80 - 200 µm/y
  - CX: 200 - 700 µm/y
- **Formula:** `Estimated Life = (Remaining_Thickness / r_corr_avg) * (1 - Corrosion_Percentage)`.

### 4.3. Status & Action Mapping
| Corrosion % | Status | Action |
|-------------|--------|--------|
| <= 40% | Aman (Green) | Inspeksi Rutin Sesuai Periode |
| 41% - 80% | Waspada (Yellow/Orange) | Intensitas Inspeksi Ditingkatkan |
| > 80% | Kritis (Red) | Perbaiki Segera |

## 5. Scope of Implementation
- Create Flask application structure.
- Implement the AI model inference logic.
- Build the responsive Bootstrap UI.
- Implement the ISO 9223 calculation engine.
- Integrate frontend-backend for real-time data input and result display.
