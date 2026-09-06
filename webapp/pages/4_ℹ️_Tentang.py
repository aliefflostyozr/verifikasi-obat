"""
4_ℹ️_Tentang.py — Tentang proyek + panduan setup lengkap dari hasil Kaggle ke Streamlit.
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from theme import page_setup, hero, section_title, icon

page_setup("Tentang & Setup — Sistem Verifikasi Obat", "ℹ️")
hero("Panduan Lengkap", "ℹ️ Tentang Proyek &amp; Cara Setup",
     "Ringkasan proyek, arsitektur sistem, dan langkah demi langkah menghubungkan hasil "
     "training Kaggle ke website ini.")

section_title("hospital", "Tentang Proyek")
st.markdown("""
**Sistem Verifikasi Obat Otomatis** adalah prototipe riset Fase 1 kerja sama
**Institut Teknologi Sepuluh Nopember (ITS)** dan **Instalasi Farmasi RSUD Haji Surabaya**.
Sistem ini memakai *computer vision* dua tahap:

1. **Detector (YOLOv8n)** — menemukan & menghitung jumlah pil pada foto meja penyiapan obat.
2. **Classifier (MobileNetV3-Small / EfficientNet / ResNet / DenseNet)** — mengenali jenis
   obat per pil yang terdeteksi (opsional, dilatih dari dataset MEDISEG).

Hasil deteksi kemudian dicocokkan dengan data **e-resep** lewat modul `eresep_matcher.py`,
menghasilkan status **SESUAI / TIDAK SESUAI / TIDAK YAKIN / GANGGUAN DATA**. Sistem ini
bersifat *human-in-the-loop* — keputusan klinis akhir selalu ada di tangan tenaga farmasi.
""")

section_title("flask", "Langkah Setup: dari Kaggle ke Website Ini")

steps = [
    ("1️⃣ Selesaikan & simpan notebook Kaggle",
     "Jalankan `pill_verification_full_pipeline.py` (atau versi .ipynb-nya) di Kaggle sampai "
     "selesai, lalu klik **Save Version → Save & Run All (Commit)**. Ini penting — tanpa "
     "Save Version, semua file di `/kaggle/working` akan hilang saat sesi berakhir."),
    ("2️⃣ Unduh paket hasil dari tab Output",
     "Buka tab **Output** notebook Kaggle setelah commit selesai. Unduh dua file:\n"
     "- `research_package_journal.zip` (semua bobot model + metrik + eksperimen jurnal)\n"
     "- `data/test_package.zip` (foto uji + manifest ground truth, untuk Dashboard Pengujian)"),
    ("3️⃣ Ekstrak ke struktur folder proyek",
     "Ekstrak isi `research_package_journal.zip` ke folder `project_root/` (folder yang sama "
     "yang berisi folder `webapp/` ini), lalu susun ulang sedikit:\n\n"
     "```\n"
     "project_root/\n"
     "├── webapp/                          <- folder ini\n"
     "│   ├── streamlit_app.py\n"
     "│   ├── runs/\n"
     "│   │   ├── detect/pill_detector/weights/best.pt      <- dari detector_main_best.pt\n"
     "│   │   └── classify_final/\n"
     "│   │       ├── best.pt                                <- dari classifier_main_best.pt\n"
     "│   │       └── class_names.json                       <- dari classifier_main_class_names.json\n"
     "│   └── ...\n"
     "├── journal_experiments/             <- dari research_package_journal.zip\n"
     "├── streamlit_manifest.json          <- dari research_package_journal.zip\n"
     "└── data/\n"
     "    └── test_package/                <- dari test_package.zip (folder photos/ + manifest.json)\n"
     "```\n\n"
     "Cara tercepat: jalankan script `setup_from_kaggle_package.py` yang disertakan dalam paket "
     "zip website ini — otomatis menaruh semua file ke lokasi yang benar:\n\n"
     "```bash\n"
     "python setup_from_kaggle_package.py \\\n"
     "    --research-zip ~/Downloads/research_package_journal.zip \\\n"
     "    --test-package-zip ~/Downloads/test_package.zip\n"
     "```"),
    ("4️⃣ Install dependency Python",
     "```bash\n"
     "pip install -r webapp/requirements.txt\n"
     "```"),
    ("5️⃣ Jalankan website",
     "```bash\n"
     "streamlit run webapp/streamlit_app.py\n"
     "```\n"
     "Buka `http://localhost:8501` di browser. Halaman **🔬 Verifikasi Foto** dan "
     "**📊 Dashboard Pengujian** akan otomatis mendeteksi model di `webapp/runs/`."),
    ("6️⃣ (Opsional) Lihat hasil riset lengkap",
     "Buka halaman **📈 Hasil Riset** dan pastikan path di sidebar menunjuk ke folder "
     "`journal_experiments/` hasil ekstraksi tadi, untuk melihat semua tabel & grafik "
     "eksperimen Q1 (baseline, ablation, latency, Grad-CAM, dll)."),
]

for title, body in steps:
    with st.expander(title, expanded=False):
        st.markdown(body)

section_title("shield", "Struktur Folder Akhir yang Diharapkan")
st.code("""
project_root/
├── webapp/
│   ├── streamlit_app.py
│   ├── theme.py
│   ├── config.py, eresep_matcher.py, visualize.py, pipeline.py
│   ├── pages/
│   │   ├── 1_🔬_Verifikasi_Foto.py
│   │   ├── 2_📊_Dashboard_Pengujian.py
│   │   ├── 3_📈_Hasil_Riset.py
│   │   └── 4_ℹ️_Tentang.py
│   ├── runs/
│   │   ├── detect/pill_detector/weights/best.pt
│   │   └── classify_final/{best.pt, class_names.json}
│   ├── requirements.txt
│   └── setup_from_kaggle_package.py
├── journal_experiments/
├── streamlit_manifest.json
└── data/test_package/{photos/, manifest.json}
""", language="text")

section_title("brain", "Catatan Metodologis (untuk naskah Q1)")
st.markdown("""
- Dataset publik yang dipakai untuk melatih model ini **hanya untuk pembuktian konsep**.
  Untuk klaim final di naskah jurnal, model wajib di-*fine-tune* dengan foto obat asli dari
  RSUD Haji sesuai tata kelola data (proposal BAB III.2).
- Halaman **📈 Hasil Riset** memuat catatan jujur soal keterbatasan tiap eksperimen
  (jumlah seed, pendekatan AP@0.75, dsb) — baca sebelum menuliskan bagian Diskusi/Limitasi.
""")
