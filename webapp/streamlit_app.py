"""
streamlit_app.py — Beranda Sistem Verifikasi Obat Otomatis.
Jalankan dengan: streamlit run webapp/streamlit_app.py
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import page_setup, hero, feature_card, icon, metric_pill, section_title
import config

page_setup("Sistem Verifikasi Obat Otomatis", "💊")

# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------
hero(
    badge="ITS × Instalasi Farmasi RSUD Haji Surabaya",
    title="💊 Sistem Verifikasi Obat Otomatis",
    subtitle=(
        "Memindai foto meja penyiapan obat, menghitung jumlah &amp; jenis pil secara otomatis, "
        "lalu mencocokkannya dengan e-resep — membantu tenaga farmasi bekerja lebih cepat, "
        "akurat, dan tetap dalam kendali manusia sepenuhnya (human-in-the-loop)."
    ),
)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown(icon("scan", 64), unsafe_allow_html=True)
    st.markdown("**1. Foto diambil**\n\nKamera memotret meja penyiapan obat sebelum diserahkan ke pasien.")
with col2:
    st.markdown(icon("brain", 64), unsafe_allow_html=True)
    st.markdown("**2. AI mendeteksi &amp; menghitung**\n\nModel computer vision mengenali tiap pil, menghitung jumlah, dan (opsional) jenisnya.", unsafe_allow_html=True)
with col3:
    st.markdown(icon("check-circle", 64), unsafe_allow_html=True)
    st.markdown("**3. Dicocokkan dengan e-resep**\n\nSistem memberi status SESUAI / TIDAK SESUAI / TIDAK YAKIN — keputusan akhir tetap di tangan apoteker.")

st.write("")

# ------------------------------------------------------------------
# STATUS MODEL (baca dari runs/ & streamlit_manifest.json kalau ada)
# ------------------------------------------------------------------
import json

manifest_path = Path(__file__).resolve().parent.parent / "streamlit_manifest.json"
detector_ready = (Path(__file__).resolve().parent / "runs" / "detect" / "pill_detector" / "weights" / "best.pt").exists()
classifier_ready = (Path(__file__).resolve().parent / "runs" / "classify_final" / "best.pt").exists()

detector_metrics = {}
classifier_metrics = {}
try:
    m = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    dm_path = Path(m.get("detector_metrics", "")) if m.get("detector_metrics") else None
    if dm_path and dm_path.exists():
        detector_metrics = json.loads(dm_path.read_text())
except Exception:
    pass

section_title("shield", "Status Sistem Saat Ini")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="green-card">{'✅' if detector_ready else '⬜'} <b>Detector (deteksi &amp; hitung pil)</b><br><span style="color:#4B6E5F">{'Siap dipakai' if detector_ready else 'Belum ditemukan — cek folder runs/'}</span></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="green-card">{'✅' if classifier_ready else '⬜'} <b>Classifier (jenis obat)</b><br><span style="color:#4B6E5F">{'Siap dipakai' if classifier_ready else 'Opsional — belum dilatih/ditemukan'}</span></div>""", unsafe_allow_html=True)
with c3:
    map50 = detector_metrics.get("mAP50")
    st.markdown(f"""<div class="green-card">📈 <b>mAP@0.5 Detector</b><br><span style="color:#146C43;font-size:1.4rem;font-weight:700">{f'{map50:.1%}' if map50 else '—'}</span></div>""", unsafe_allow_html=True)
with c4:
    prec = detector_metrics.get("precision")
    st.markdown(f"""<div class="green-card">🎯 <b>Precision Detector</b><br><span style="color:#146C43;font-size:1.4rem;font-weight:700">{f'{prec:.1%}' if prec else '—'}</span></div>""", unsafe_allow_html=True)

if not detector_ready:
    st.info(
        "Model detector belum ditemukan di `webapp/runs/detect/pill_detector/weights/best.pt`. "
        "Buka halaman **⚙️ Tentang & Setup** di sidebar untuk panduan lengkap menyiapkan model "
        "hasil training Kaggle."
    )

st.write("")

# ------------------------------------------------------------------
# FITUR UTAMA
# ------------------------------------------------------------------
section_title("flask", "Fitur Utama")
f1, f2, f3 = st.columns(3)
with f1:
    feature_card("scan", "🔬 Verifikasi Foto",
                  "Upload satu foto meja penyiapan obat + data e-resep, dan lihat hasil deteksi, "
                  "jumlah pil, serta status kecocokan secara instan.")
with f2:
    feature_card("chart", "📊 Dashboard Pengujian",
                  "Uji sistem secara batch pada ratusan foto sekaligus, lengkap dengan akurasi, "
                  "confusion matrix, dan distribusi status.")
with f3:
    feature_card("brain", "📈 Hasil Riset",
                  "Lihat seluruh metrik ilmiah dari pipeline Kaggle: perbandingan arsitektur, "
                  "ablation study, uji signifikansi, hingga Grad-CAM explainability.")

st.write("")
section_title("hospital", "Mengapa Ini Penting")
g1, g2, g3 = st.columns(3)
with g1:
    metric_pill("⏱️", "Memangkas waktu tunggu verifikasi manual di instalasi farmasi")
with g2:
    metric_pill("🧠", "Human-in-the-loop — sistem membantu, keputusan klinis tetap di apoteker")
with g3:
    metric_pill("🔁", "Fail-safe by design — data e-resep tak lengkap → tidak pernah otomatis \"SESUAI\"")

st.write("")
st.caption(
    "Prototipe riset Fase 1 — ITS × Instalasi Farmasi RSUD Haji Surabaya. "
    "Dataset publik dipakai untuk pembuktian konsep; pemakaian produksi wajib fine-tuning "
    "dengan data asli sesuai tata kelola data (proposal BAB III.2)."
)
