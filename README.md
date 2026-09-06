# Sistem Verifikasi Obat Otomatis — Website (Streamlit)

Website ini adalah antarmuka demo untuk sistem verifikasi obat otomatis
(ITS x Instalasi Farmasi RSUD Haji Surabaya). Ada 4 halaman:

1. **Beranda** — ringkasan sistem & status model.
2. **🔬 Verifikasi Foto** — upload 1 foto + e-resep, lihat hasil verifikasi instan.
3. **📊 Dashboard Pengujian** — uji batch pada banyak foto sekaligus (akurasi, confusion matrix).
4. **📈 Hasil Riset** — tabel & grafik seluruh eksperimen Q1 (baseline, ablation, latency, Grad-CAM, dll).
5. **ℹ️ Tentang & Setup** — panduan lengkap (juga tersedia di dalam aplikasi).

## Quick start

```bash
# 1) Setelah notebook Kaggle selesai & di-"Save Version", unduh dari tab Output:
#    - research_package_journal.zip
#    - data/test_package.zip

# 2) Taruh file zip itu di mana saja, lalu jalankan dari folder project ini:
python setup_from_kaggle_package.py \
    --research-zip /path/ke/research_package_journal.zip \
    --test-package-zip /path/ke/test_package.zip

# 3) Install dependency
pip install -r webapp/requirements.txt

# 4) Jalankan
streamlit run webapp/streamlit_app.py
```

Buka `http://localhost:8501`. Detail lengkap ada di halaman **ℹ️ Tentang & Setup**
di dalam aplikasi.

## Struktur folder

```
project_root/
├── webapp/                  <- kode Streamlit
│   ├── streamlit_app.py     <- halaman Beranda (entry point)
│   ├── theme.py             <- tema hijau + komponen UI bersama
│   ├── config.py, eresep_matcher.py, visualize.py, pipeline.py
│   ├── pages/                <- 4 halaman lainnya
│   ├── runs/                 <- diisi otomatis oleh setup_from_kaggle_package.py
│   └── requirements.txt
├── setup_from_kaggle_package.py
├── journal_experiments/     <- diisi otomatis (hasil eksperimen Q1)
├── streamlit_manifest.json  <- diisi otomatis
└── data/test_package/       <- diisi otomatis (foto uji + manifest)
```
