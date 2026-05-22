# Design Spec: PLN UIP3BKAL Corrosion Monitoring System (Cloud Migration)

## 1. Overview
Sistem monitoring korosi yang saat ini berjalan lokal akan dimigrasikan ke arsitektur Cloud agar dapat diakses 24 jam dan mendukung penyimpanan foto skala besar (>10GB) menggunakan Google Drive 5TB milik user.

## 2. Arsitektur Sistem
- **Frontend/Backend:** Flask (Python 3.11+) yang dideploy di **Render**.
- **Database (Metadata):** **Supabase (PostgreSQL)** untuk menyimpan data teks dan link file.
- **Object Storage (Images):** **Google Drive (5TB)** via Google Drive API.
- **CI/CD:** GitHub Integration (Otomatis deploy saat ada push ke main branch).

## 3. Data Schema (Supabase)
Tabel: `corrosion_data`
- `id`: UUID (Primary Key)
- `created_at`: Timestamp
- `tower_name`: String
- `circuit`: String
- `accessory`: String
- `inspection_date`: Date
- `corrosion_level`: String (Input user)
- `ai_percentage`: Float (Hasil analisis AI)
- `remaining_life`: Float
- `status`: String (Aman/Waspada/Kritis)
- `gdrive_file_id`: String (ID file di Google Drive untuk menampilkan gambar)

## 4. Alur Kerja (Workflow)
1. **Upload:** User mengisi form dan upload foto di web.
2. **AI Analysis:** Flask memproses foto secara lokal di server Render menggunakan model TensorFlow yang sudah ada.
3. **Cloud Storage:** Flask mengunggah foto ke folder spesifik di Google Drive menggunakan *Service Account*.
4. **Persistence:** Data hasil analisis dan `gdrive_file_id` disimpan ke Supabase.
5. **Display:** Dashboard mengambil data dari Supabase dan menghasilkan link pratinjau gambar dari ID Google Drive.

## 5. Komponen Keamanan
- **Environment Variables:** Semua kunci API (Supabase URL/Key, GDrive JSON) akan disimpan di Render Environment Variables, bukan di kode GitHub.
- **Service Account:** Menggunakan akun layanan Google dengan akses terbatas hanya ke folder tertentu di Google Drive.

## 6. Rencana Implementasi
1. Setup Project di Google Cloud Console & Aktifkan GDrive API.
2. Setup Database di Supabase.
3. Refaktor `app.py` untuk mendukung `google-api-python-client` dan `supabase-py`.
4. Deploy ke Render melalui GitHub.
