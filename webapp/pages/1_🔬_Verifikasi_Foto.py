"""
1_🔬_Verifikasi_Foto.py — Upload satu foto + e-resep, jalankan pipeline verifikasi.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from theme import page_setup, hero, section_title, status_chip, icon
import config

page_setup("Verifikasi Foto — Sistem Verifikasi Obat", "🔬")
hero("Verifikasi Instan", "🔬 Verifikasi Foto Meja Penyiapan Obat",
     "Upload satu foto, isi daftar e-resep, dan sistem akan mendeteksi, menghitung, "
     "lalu mencocokkannya secara otomatis dalam hitungan detik.")

WEBAPP_DIR = Path(__file__).resolve().parent.parent
DETECTOR_PATH_DEFAULT = str(WEBAPP_DIR / "runs" / "detect" / "pill_detector" / "weights" / "best.pt")
CLASSIFIER_PATH_DEFAULT = str(WEBAPP_DIR / "runs" / "classify_final" / "best.pt")
CLASSIFIER_CLASSES_DEFAULT = str(WEBAPP_DIR / "runs" / "classify_final" / "class_names.json")

with st.sidebar:
    section_title("shield", "Konfigurasi Model")
    detector_path = st.text_input("Path bobot detector (.pt)", value=DETECTOR_PATH_DEFAULT)
    use_classifier = st.checkbox("Pakai classifier jenis obat (kalau tersedia)", value=Path(CLASSIFIER_PATH_DEFAULT).exists())
    classifier_path = st.text_input("Path bobot classifier (.pt) — opsional",
                                     value=CLASSIFIER_PATH_DEFAULT if use_classifier else "")
    classifier_classes_path = st.text_input("Path class_names.json — opsional",
                                             value=CLASSIFIER_CLASSES_DEFAULT if use_classifier else "")
    conf_th = st.slider("Confidence threshold deteksi", 0.05, 0.9, config.DETECTOR_CONF_THRESHOLD, 0.05)

if not Path(detector_path).exists():
    st.error(
        f"Bobot detector tidak ditemukan di `{detector_path}`. Buka halaman **Tentang & Setup** "
        f"di sidebar bawah untuk panduan menyiapkan model hasil training Kaggle."
    )
    st.stop()


@st.cache_resource(show_spinner="Memuat model ke memori...")
def load_pipeline(det_path, cls_path, cls_classes_path):
    from pipeline import PillVerificationPipeline
    return PillVerificationPipeline(
        detector_weights=det_path,
        classifier_weights=cls_path if cls_path and Path(cls_path).exists() else None,
        classifier_classes_json=cls_classes_path if cls_classes_path and Path(cls_classes_path).exists() else None,
    )


pipeline = load_pipeline(detector_path, classifier_path, classifier_classes_path)
config.DETECTOR_CONF_THRESHOLD = conf_th

section_title("scan", "1. Upload Foto")
uploaded_photo = st.file_uploader("Foto meja penyiapan obat", type=["jpg", "jpeg", "png", "bmp"])

section_title("flask", "2. Data E-Resep")
st.caption("Tambahkan setiap jenis obat beserta jumlah yang seharusnya ada sesuai e-resep.")

if "eresep_rows" not in st.session_state:
    st.session_state.eresep_rows = [{"nama_obat": "pill", "jumlah": 5}]

for i, row in enumerate(st.session_state.eresep_rows):
    c1, c2, c3 = st.columns([3, 2, 1])
    row["nama_obat"] = c1.text_input(f"Nama obat #{i+1}", value=row["nama_obat"], key=f"nama_{i}")
    row["jumlah"] = c2.number_input(f"Jumlah #{i+1}", min_value=0, value=int(row["jumlah"]), key=f"jml_{i}")
    if c3.button("🗑️ Hapus", key=f"del_{i}") and len(st.session_state.eresep_rows) > 1:
        st.session_state.eresep_rows.pop(i)
        st.rerun()

if st.button("➕ Tambah obat"):
    st.session_state.eresep_rows.append({"nama_obat": "", "jumlah": 0})
    st.rerun()

st.write("")
run_clicked = st.button("🚀 Jalankan Verifikasi", type="primary", width="stretch")

if run_clicked:
    if uploaded_photo is None:
        st.warning("Upload foto dulu sebelum menjalankan verifikasi.")
        st.stop()

    eresep_items = [{"nama_obat": r["nama_obat"], "jumlah": r["jumlah"]}
                     for r in st.session_state.eresep_rows if r["nama_obat"]]

    file_bytes = np.frombuffer(uploaded_photo.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    tmp_path = WEBAPP_DIR / "_tmp_upload.jpg"
    cv2.imwrite(str(tmp_path), img)

    with st.spinner("Mendeteksi & mencocokkan..."):
        output = pipeline.verify_against_eresep(str(tmp_path), eresep_items)
    tmp_path.unlink(missing_ok=True)

    match = output["match"]
    section_title("check-circle", "3. Hasil Verifikasi")
    st.markdown(status_chip(match.status), unsafe_allow_html=True)
    st.caption(match.catatan)

    col_img, col_detail = st.columns([3, 2])
    with col_img:
        annotated_rgb = cv2.cvtColor(output["annotated_image"], cv2.COLOR_BGR2RGB)
        st.image(annotated_rgb, caption="Hasil deteksi (kotak hijau=sesuai, merah=tidak sesuai, oranye=tidak yakin)",
                  width="stretch")
    with col_detail:
        st.markdown("**Rincian per jenis obat**")
        for item in match.detail_per_obat:
            conf_str = f"{item['confidence']:.0%}" if item["confidence"] is not None else "—"
            st.markdown(f"""
            <div class="green-card" style="margin-bottom:10px;">
            <b>{item['nama_obat']}</b><br>
            E-resep: {item['jumlah_resep']} &nbsp;|&nbsp; Terdeteksi: {item['jumlah_terdeteksi']} &nbsp;|&nbsp; Conf: {conf_str}<br>
            {status_chip(item['status'])}
            </div>
            """, unsafe_allow_html=True)
