"""
3_📈_Hasil_Riset.py — Menampilkan seluruh hasil eksperimen riset (baseline, ablation,
uji signifikansi, latency, error analysis, Grad-CAM) dari paket hasil Kaggle,
kalau sudah diunduh & ditaruh di folder yang benar.
"""
import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from theme import page_setup, hero, section_title, icon

page_setup("Hasil Riset — Sistem Verifikasi Obat", "📈")
hero("Untuk Naskah Jurnal Q1", "📈 Hasil Riset & Eksperimen Ilmiah",
     "Ringkasan seluruh eksperimen dari pipeline Kaggle: perbandingan baseline/SOTA, "
     "ablation study, uji signifikansi statistik, latency benchmark, error analysis, "
     "dan explainability — siap dijadikan Tabel/Gambar naskah.")

WEBAPP_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = WEBAPP_DIR.parent
default_journal_dir = st.sidebar.text_input(
    "Path folder journal_experiments (dari research_package_journal.zip)",
    value=str(PROJECT_ROOT / "journal_experiments"),
)
JOURNAL_DIR = Path(default_journal_dir)


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def show_image_if_exists(path: Path, caption: str = ""):
    if path.exists():
        st.image(str(path), caption=caption, width="stretch")
        return True
    return False


def _label(key: str) -> str:
    return key.replace("_", " ").strip().title()


def render_ci_table(d: dict, name_col: str = "Skema/Kategori"):
    """Render dict berisi {nama: {mean, std, low, high, n}} sebagai tabel rapi."""
    rows = []
    for k, v in d.items():
        rows.append({
            name_col: _label(k),
            "Mean": round(v.get("mean", 0), 4),
            "95% CI": f"[{v.get('low', 0):.4f}, {v.get('high', 0):.4f}]",
            "n": v.get("n", "-"),
        })
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def render_summary_dict(d: dict):
    """
    Render dict hasil eksperimen secara rapi tanpa menampilkan JSON mentah:
    - Nilai skalar (angka/boolean) -> st.metric berjajar
    - Nilai berbentuk {mean, low, high, n, ...} -> tabel dengan kolom 95% CI
    - Nilai berbentuk list of dict -> tabel biasa (diurutkan kalau ada kolom 'count')
    - Sisanya -> ditampilkan sebagai teks/tabel sebisa mungkin, baru fallback ke st.json
    """
    scalar_items, ci_items, table_items, other_items = {}, {}, {}, {}
    for k, v in d.items():
        if isinstance(v, dict) and "mean" in v:
            ci_items[k] = v
        elif isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
            table_items[k] = v
        elif isinstance(v, (int, float, bool, str)):
            scalar_items[k] = v
        else:
            other_items[k] = v

    if scalar_items:
        cols = st.columns(len(scalar_items))
        for col, (k, v) in zip(cols, scalar_items.items()):
            if isinstance(v, bool):
                col.metric(_label(k), "✅ Ya" if v else "❌ Tidak")
            elif isinstance(v, float):
                col.metric(_label(k), f"{v:,.2f}")
            else:
                col.metric(_label(k), v)

    if ci_items:
        render_ci_table(ci_items)

    for k, v in table_items.items():
        st.markdown(f"**{_label(k)}** — total {len(v)} baris")
        df = pd.DataFrame(v)
        if "count" in df.columns:
            df = df.sort_values("count", ascending=False)
        st.dataframe(df, width="stretch", hide_index=True)

    for k, v in other_items.items():
        if isinstance(v, dict) and v:
            st.markdown(f"**{_label(k)}**")
            try:
                df = pd.DataFrame([v])
                st.dataframe(df, width="stretch", hide_index=True)
            except Exception:
                st.json(v)
        elif v not in (None, {}, []):
            st.write(f"**{_label(k)}**: {v}")


if not JOURNAL_DIR.exists():
    st.warning(
        f"Folder eksperimen belum ditemukan di `{JOURNAL_DIR}`. Ekstrak "
        f"`research_package_journal.zip` hasil Kaggle, lalu arahkan path di sidebar "
        f"ke folder `journal_experiments` di dalamnya."
    )
    st.stop()

tabs = st.tabs(["🏆 Baseline/SOTA", "🧪 Ablation Study", "⚡ Latency", "🩺 Data Asli RSUD",
                 "🔍 Error Analysis", "🧠 Explainability", "🔗 Simulasi E-Resep"])

# --- 1. Baseline ---
with tabs[0]:
    section_title("chart", "Perbandingan Arsitektur Detector & Classifier")
    det = load_json(JOURNAL_DIR / "detector_baseline" / "baseline_summary.json")
    if det:
        st.markdown("**Detector**")
        rows = []
        for name, s in det.get("summary", {}).items():
            row = {"Model": name, "n_seed": s.get("n_seeds", "-")}
            if "mAP50" in s:
                row["mAP50 (mean)"] = round(s["mAP50"]["mean"], 4)
            if "mAP50_95" in s:
                row["mAP50-95 (mean)"] = round(s["mAP50_95"]["mean"], 4)
                row["95% CI (mAP50-95)"] = f"[{s['mAP50_95']['low']:.4f}, {s['mAP50_95']['high']:.4f}]"
            if "precision" in s:
                row["Precision"] = round(s["precision"]["mean"], 4)
            if "recall" in s:
                row["Recall"] = round(s["recall"]["mean"], 4)
            if "mean_train_time_sec" in s:
                row["Waktu latih (s)"] = round(s["mean_train_time_sec"], 1)
            rows.append(row)
        if rows:
            st.dataframe(pd.DataFrame(rows), width="stretch")
        show_image_if_exists(JOURNAL_DIR / "detector_baseline" / "baseline_comparison.png")
        sig = det.get("significance_tests_mAP50_95", {})
        if sig:
            st.markdown("**Uji signifikansi (bootstrap, berpasangan) — mAP50-95**")
            st.dataframe(pd.DataFrame(sig).T, width="stretch")
    else:
        st.info("Hasil baseline detector belum tersedia di folder ini.")

    cls_ = load_json(JOURNAL_DIR / "classifier_baseline" / "classifier_baseline_summary.json")
    if cls_:
        st.markdown("**Classifier**")
        rows = []
        for name, s in cls_.get("summary", {}).items():
            row = {"Arsitektur": name, "n_seed": s.get("n_seeds", "-")}
            if "accuracy" in s:
                row["Accuracy"] = round(s["accuracy"]["mean"], 4)
            if "macro_f1" in s:
                row["Macro F1 (mean)"] = round(s["macro_f1"]["mean"], 4)
                row["95% CI (Macro F1)"] = f"[{s['macro_f1']['low']:.4f}, {s['macro_f1']['high']:.4f}]"
            if "auc_roc_ovr_macro" in s:
                row["AUC-ROC"] = round(s["auc_roc_ovr_macro"]["mean"], 4)
            rows.append(row)
        if rows:
            st.dataframe(pd.DataFrame(rows), width="stretch")
        show_image_if_exists(JOURNAL_DIR / "classifier_baseline" / "classifier_baseline_comparison.png")

# --- 2. Ablation ---
with tabs[1]:
    section_title("flask", "Ablation Study")
    st.markdown("**Ukuran model × Resolusi × Confidence threshold**")
    abl1 = load_json(JOURNAL_DIR / "ablation_model_res_conf" / "ablation_model_res_conf.json")
    if abl1:
        st.dataframe(pd.DataFrame(abl1), width="stretch", height=260)
    show_image_if_exists(JOURNAL_DIR / "ablation_model_res_conf" / "ablation_accuracy_vs_latency.png",
                          "Trade-off akurasi vs latensi")

    st.markdown("**Pengaruh augmentasi data**")
    abl2 = load_json(JOURNAL_DIR / "ablation_augmentation" / "ablation_augmentation.json")
    if abl2:
        st.dataframe(pd.DataFrame(abl2), width="stretch")

    st.markdown("**Skema pretrain classifier (tanpa pretrain vs CURE vs MEDISEG finetune)**")
    abl3 = load_json(JOURNAL_DIR / "pretrain_scheme_ablation" / "pretrain_scheme_summary.json")
    if abl3:
        render_ci_table(abl3, name_col="Skema Pretrain")
    else:
        st.info("Hasil ablation skema pretrain belum tersedia di folder ini.")

# --- 3. Latency ---
with tabs[2]:
    section_title("clock", "Latency Benchmark End-to-End")
    lat = load_json(JOURNAL_DIR / "latency" / "latency_results.json")
    if lat:
        rows = []
        for dev, batches in lat.items():
            # Struktur bisa 2 level (device -> batch -> stats) atau 1 level (device -> stats)
            if isinstance(batches, dict) and all(isinstance(v, dict) for v in batches.values()):
                for batch_name, stats in batches.items():
                    rows.append({"Device": dev, "Batch": batch_name, **stats})
            else:
                rows.append({"Device": dev, **batches})
        st.dataframe(pd.DataFrame(rows), width="stretch")
        show_image_if_exists(JOURNAL_DIR / "latency" / "latency_vs_batch_size.png",
                              "Latensi vs ukuran batch (CPU vs GPU)")
    else:
        st.info("Hasil latency benchmark belum tersedia di folder ini.")

# --- 4. Real hospital data ---
with tabs[3]:
    section_title("hospital", "Evaluasi pada Data Asli RSUD Haji")
    real = load_json(JOURNAL_DIR / "real_hospital_eval" / "real_hospital_eval_results.json")
    if real:
        render_summary_dict(real)
    else:
        st.info(
            "Belum ada hasil evaluasi data asli. Nanti akan ditambahkan data asli jika sudah ada"
        )

# --- 5. Error analysis ---
with tabs[4]:
    section_title("scan", "Error Analysis")
    st.markdown("**Detector — kategori False Positive / False Negative**")
    err_det = load_json(JOURNAL_DIR / "error_analysis_detector" / "detector_error_report.json")
    if err_det:
        kategori = err_det.get("kategori_error", {})
        if kategori:
            df_kat = pd.DataFrame(
                sorted(kategori.items(), key=lambda x: x[1], reverse=True),
                columns=["Kategori Error", "Jumlah"],
            )
            df_kat["Kategori Error"] = df_kat["Kategori Error"].map(_label)
            c1, c2 = st.columns([2, 1])
            with c1:
                st.dataframe(df_kat, width="stretch", hide_index=True)
            with c2:
                st.metric("FN Contoh Disimpan", err_det.get("n_fn_examples_disimpan", "-"))
                st.metric("FP Contoh Disimpan", err_det.get("n_fp_examples_disimpan", "-"))
    show_image_if_exists(JOURNAL_DIR / "error_analysis_detector" / "error_category_distribution.png",
                          "Distribusi kategori error")
    c1, c2 = st.columns(2)
    with c1:
        show_image_if_exists(JOURNAL_DIR / "error_analysis_detector" / "fn_examples_montage.png",
                              "Contoh False Negative")
    with c2:
        show_image_if_exists(JOURNAL_DIR / "error_analysis_detector" / "fp_examples_montage.png",
                              "Contoh False Positive")

    st.markdown("**Classifier — pasangan kelas paling sering tertukar**")
    err_cls = load_json(JOURNAL_DIR / "error_analysis_classifier" / "classifier_error_report.json")
    if err_cls:
        st.metric("Total Salah Klasifikasi", err_cls.get("n_misclassified_total", "-"))
        pairs = err_cls.get("top_confusion_pairs", [])
        if pairs:
            df_pairs = pd.DataFrame(pairs).rename(
                columns={"true": "Kelas Asli", "pred": "Diprediksi Sebagai", "count": "Jumlah"}
            )
            df_pairs = df_pairs.sort_values("Jumlah", ascending=False)
            st.dataframe(df_pairs, width="stretch", hide_index=True)
    show_image_if_exists(JOURNAL_DIR / "error_analysis_classifier" / "misclassified_montage.png",
                          "Contoh crop yang salah diklasifikasi")

# --- 6. Explainability ---
with tabs[5]:
    section_title("brain", "Explainability — Grad-CAM")
    st.caption("Area gambar yang paling memengaruhi keputusan classifier (merah = paling berpengaruh).")
    c1, c2 = st.columns(2)
    with c1:
        show_image_if_exists(JOURNAL_DIR / "explainability" / "gradcam_correct_examples.png", "Contoh prediksi BENAR")
    with c2:
        show_image_if_exists(JOURNAL_DIR / "explainability" / "gradcam_incorrect_examples.png", "Contoh prediksi SALAH")

# --- 7. E-resep simulation ---
with tabs[6]:
    section_title("flask", "Simulasi Integrasi E-Resep")
    sim = load_json(JOURNAL_DIR / "eresep_simulation" / "eresep_integration_summary.json")
    if sim:
        render_summary_dict(sim)
    show_image_if_exists(JOURNAL_DIR / "eresep_simulation" / "alur_integrasi_eresep.png", "Alur data end-to-end")
