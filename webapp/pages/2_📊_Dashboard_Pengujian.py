"""
2_📊_Dashboard_Pengujian.py — Uji sistem secara batch pada test_package (foto + manifest ground truth).
"""
import json
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from theme import page_setup, hero, section_title, status_chip, icon
import config

page_setup("Dashboard Pengujian — Sistem Verifikasi Obat", "📊")
hero("Pengujian Batch", "📊 Dashboard Pengujian Sistem",
     "Jalankan pengujian pada ratusan foto sekaligus dan lihat akurasi, confusion matrix, "
     "serta distribusi status secara langsung — cocok untuk validasi sebelum deployment.")

WEBAPP_DIR = Path(__file__).resolve().parent.parent
DETECTOR_PATH_DEFAULT = str(WEBAPP_DIR / "runs" / "detect" / "pill_detector" / "weights" / "best.pt")
CLASSIFIER_PATH_DEFAULT = str(WEBAPP_DIR / "runs" / "classify_final" / "best.pt")
CLASSIFIER_CLASSES_DEFAULT = str(WEBAPP_DIR / "runs" / "classify_final" / "class_names.json")
TEST_PACKAGE_DEFAULT = str(WEBAPP_DIR.parent / "data" / "test_package")

with st.sidebar:
    section_title("shield", "Konfigurasi Model")
    detector_path = st.text_input("Path bobot detector (.pt)", value=DETECTOR_PATH_DEFAULT)
    classifier_path = st.text_input("Path bobot classifier (.pt) — opsional",
                                     value=CLASSIFIER_PATH_DEFAULT if Path(CLASSIFIER_PATH_DEFAULT).exists() else "")
    classifier_classes_path = st.text_input("Path class_names.json — opsional",
                                             value=CLASSIFIER_CLASSES_DEFAULT if Path(CLASSIFIER_CLASSES_DEFAULT).exists() else "")

    st.markdown("---")
    section_title("flask", "Sumber Data Uji")
    source_mode = st.radio("Foto uji diambil dari mana?", ["Folder lokal (jalan di komputer/server yang sama)", "Upload dari browser"])
    test_folder = None
    manifest_text = None
    uploaded_photos = None

    if source_mode.startswith("Folder"):
        test_folder = st.text_input("Path folder test_package (berisi photos/ + manifest.json)",
                                     value=TEST_PACKAGE_DEFAULT)
    else:
        uploaded_photos = st.file_uploader("Upload semua foto uji", type=["jpg", "jpeg", "png", "bmp"],
                                            accept_multiple_files=True)
        manifest_text = st.text_area("Paste isi manifest.json di sini", height=160,
                                      placeholder='[{"image": "foto1.jpg", "eresep": [...], "expected_status": "SESUAI"}]')

    run_batch = st.button("🚀 Jalankan Pengujian Batch", type="primary", use_container_width=True)

if not Path(detector_path).exists():
    st.error(f"Bobot detector tidak ditemukan di `{detector_path}`. Cek halaman **Tentang & Setup**.")
    st.stop()


@st.cache_resource(show_spinner="Memuat model ke memori...")
def load_pipeline(det_path, cls_path, cls_classes_path):
    from pipeline import PillVerificationPipeline
    return PillVerificationPipeline(
        detector_weights=det_path,
        classifier_weights=cls_path if cls_path and Path(cls_path).exists() else None,
        classifier_classes_json=cls_classes_path if cls_classes_path and Path(cls_classes_path).exists() else None,
    )


def load_manifest_and_photos():
    """Mengembalikan list of dict {image_path (Path), eresep, expected_status} atau None."""
    entries = []
    if source_mode.startswith("Folder"):
        base = Path(test_folder)
        manifest_path = base / "manifest.json"
        photos_dir = base / "photos"
        if not manifest_path.exists():
            st.error(f"`manifest.json` tidak ditemukan di `{base}`.")
            return None
        if not photos_dir.exists():
            st.error(f"Folder `photos/` tidak ditemukan di `{base}`.")
            return None
        manifest = json.loads(manifest_path.read_text())
        for m in manifest:
            img_path = photos_dir / m["image"]
            if img_path.exists():
                entries.append({"image_path": img_path, "eresep": m["eresep"],
                                 "expected_status": m.get("expected_status")})
    else:
        if not uploaded_photos:
            st.error("Upload foto uji terlebih dahulu.")
            return None
        if not manifest_text or not manifest_text.strip():
            st.error("Paste isi manifest.json terlebih dahulu.")
            return None
        try:
            manifest = json.loads(manifest_text)
        except Exception as e:
            st.error(f"manifest.json tidak valid: {e}")
            return None
        photo_map = {f.name: f for f in uploaded_photos}
        tmp_dir = WEBAPP_DIR / "_tmp_batch_upload"
        tmp_dir.mkdir(exist_ok=True)
        for m in manifest:
            f = photo_map.get(m["image"])
            if f is None:
                continue
            dest = tmp_dir / m["image"]
            dest.write_bytes(f.getvalue())
            entries.append({"image_path": dest, "eresep": m["eresep"],
                             "expected_status": m.get("expected_status")})
    return entries


if run_batch:
    entries = load_manifest_and_photos()
    if entries:
        pipeline = load_pipeline(detector_path, classifier_path, classifier_classes_path)
        progress = st.progress(0, text="Memulai pengujian batch...")
        rows = []
        t_start = time.time()
        for i, e in enumerate(entries):
            t0 = time.time()
            try:
                out = pipeline.verify_against_eresep(str(e["image_path"]), e["eresep"])
                pred_status = out["match"].status
            except Exception as ex:
                pred_status = "ERROR"
            latency_ms = (time.time() - t0) * 1000
            rows.append({
                "image": e["image_path"].name,
                "expected_status": e.get("expected_status"),
                "predicted_status": pred_status,
                "latency_ms": latency_ms,
            })
            progress.progress((i + 1) / len(entries), text=f"Memproses foto {i+1}/{len(entries)}...")
        total_time = time.time() - t_start
        progress.empty()
        df = pd.DataFrame(rows)
        st.session_state["batch_results_df"] = df
        st.session_state["batch_total_time"] = total_time

if "batch_results_df" in st.session_state:
    df = st.session_state["batch_results_df"]
    total_time = st.session_state.get("batch_total_time", 0)

    section_title("chart", "Hasil Pengujian Batch")
    n = len(df)
    has_gt = df["expected_status"].notna().any()

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="green-card">📷 <b>Total foto</b><br><span style="font-size:1.5rem;font-weight:700;color:#146C43">{n}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="green-card">⏱️ <b>Total waktu</b><br><span style="font-size:1.5rem;font-weight:700;color:#146C43">{total_time:.1f}s</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="green-card">⚡ <b>Rata-rata / foto</b><br><span style="font-size:1.5rem;font-weight:700;color:#146C43">{df["latency_ms"].mean():.0f}ms</span></div>', unsafe_allow_html=True)

    if has_gt:
        valid = df[df["expected_status"].notna()]
        acc = (valid["expected_status"] == valid["predicted_status"]).mean()
        c4.markdown(f'<div class="green-card">🎯 <b>Akurasi vs ground truth</b><br><span style="font-size:1.5rem;font-weight:700;color:#146C43">{acc:.1%}</span></div>', unsafe_allow_html=True)
    else:
        c4.markdown('<div class="green-card">ℹ️ <b>Ground truth</b><br><span style="color:#4B6E5F">Tidak tersedia (expected_status kosong)</span></div>', unsafe_allow_html=True)

    st.write("")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Distribusi status prediksi**")
        st.bar_chart(df["predicted_status"].value_counts())

    if has_gt:
        with col_b:
            st.markdown("**Confusion Matrix (expected vs predicted)**")
            labels = sorted(set(df["expected_status"].dropna()) | set(df["predicted_status"]))
            cm = pd.crosstab(df["expected_status"], df["predicted_status"]).reindex(
                index=labels, columns=labels, fill_value=0)
            st.dataframe(cm, use_container_width=True)

    st.write("")
    st.markdown("**Rincian per foto**")
    st.dataframe(df, use_container_width=True, height=320)
    st.download_button("⬇️ Unduh hasil (CSV)", df.to_csv(index=False), "hasil_pengujian_batch.csv", "text/csv")
