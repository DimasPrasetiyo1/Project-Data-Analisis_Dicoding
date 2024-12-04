# Project-Data-Analisis_Dicoding

# Project Data Analisis Dicoding

## Deskripsi
Proyek ini bertujuan untuk menganalisis data kualitas udara di Beijing (PRSA Data) dan menampilkan hasilnya melalui dashboard interaktif.

## Struktur Folder
- **dashboard/**: Folder yang berisi file Python untuk menjalankan dashboard.
  - `dashboard.py`: Script utama untuk menjalankan dashboard interaktif.
- **data/**: Folder yang berisi data mentah dan data yang sudah dibersihkan.
  - `PRSA_Data_20130301-20170228`: Data mentah dalam format CSV.
  - `clean_data.xlsx`: Data yang sudah dibersihkan dalam format Excel.
- `notebook.ipynb`: Notebook Jupyter untuk eksplorasi dan analisis data.
- `README.md`: File dokumentasi proyek ini.
- `requirements.txt`: File yang berisi daftar dependensi Python yang diperlukan.

## Persyaratan
1. Python 3.7 atau versi yang lebih baru.
2. Semua library yang tercantum di `requirements.txt`.

## Instalasi dan Cara Menjalankan
1. Clone repository ini ke lokal Anda:
   ```bash
   git clone <https://github.com/DimasPrasetiyo1/Project-Data-Analisis_Dicoding.git>
   cd PROJECT-DATA-ANALISIS_DICODING

Buat environment virtual (opsional tetapi disarankan):

```bash
# Membuat environment virtual
python -m venv venv

# Aktivasi environment virtual
source venv/bin/activate   # Untuk Linux/Mac
venv\Scripts\activate      # Untuk Windows

# Instal dependensi
pip install -r requirements.txt

# Jalankan file dashboard.py
streamlit run dashboard.py

# Buka browser Anda dan akses dashboard melalui alamat yang tertera di terminal,
# biasanya http://127.0.0.1:8050

