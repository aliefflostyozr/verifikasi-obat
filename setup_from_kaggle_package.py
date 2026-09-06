"""
setup_from_kaggle_package.py
=============================
Menyiapkan struktur folder lokal secara otomatis dari hasil unduhan Kaggle
(`research_package_journal.zip` dan/atau `test_package.zip`), supaya
`webapp/streamlit_app.py` langsung bisa jalan tanpa mindah-mindah file manual.

Jalankan dari folder project_root/ (folder yang berisi folder webapp/ ini):

    python setup_from_kaggle_package.py \\
        --research-zip ~/Downloads/research_package_journal.zip \\
        --test-package-zip ~/Downloads/test_package.zip
"""
import argparse
import json
import shutil
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEBAPP_DIR = PROJECT_ROOT / "webapp"


def extract_zip(zip_path: Path, dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest_dir)
    print(f"  Diekstrak ke: {dest_dir}")


def setup_research_package(zip_path: Path):
    print(f"\n[1] Mengekstrak {zip_path.name} ...")
    tmp = PROJECT_ROOT / ".tmp_research_package"
    if tmp.exists():
        shutil.rmtree(tmp)
    extract_zip(zip_path, tmp)

    # --- detector weights ---
    detector_src = tmp / "detector_main_best.pt"
    if detector_src.exists():
        dest = WEBAPP_DIR / "runs" / "detect" / "pill_detector" / "weights" / "best.pt"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(detector_src, dest)
        print(f"  Bobot DETECTOR -> {dest}")
    else:
        print("  [!] detector_main_best.pt tidak ditemukan di paket.")

    # --- classifier weights (opsional) ---
    cls_src = tmp / "classifier_main_best.pt"
    cls_classes_src = tmp / "classifier_main_class_names.json"
    if cls_src.exists() and cls_classes_src.exists():
        dest_dir = WEBAPP_DIR / "runs" / "classify_final"
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cls_src, dest_dir / "best.pt")
        shutil.copy2(cls_classes_src, dest_dir / "class_names.json")
        print(f"  Bobot CLASSIFIER -> {dest_dir}")
    else:
        print("  [i] Classifier tidak ditemukan di paket -- wajar kalau belum sempat dilatih.")

    # --- metrics ---
    for fname, dest_name in [("detector_main_metrics.json", "detector_metrics.json"),
                              ("classifier_main_metrics.json", "classifier_metrics.json")]:
        src = tmp / fname
        if src.exists():
            dest = PROJECT_ROOT / dest_name
            shutil.copy2(src, dest)
            print(f"  {fname} -> {dest}")

    # --- journal experiments folder ---
    journal_src = tmp / "journal_experiments"
    if journal_src.exists():
        journal_dest = PROJECT_ROOT / "journal_experiments"
        if journal_dest.exists():
            shutil.rmtree(journal_dest)
        shutil.copytree(journal_src, journal_dest)
        print(f"  journal_experiments/ -> {journal_dest}")

    # --- eda plots ---
    eda_src = tmp / "eda_plots"
    if eda_src.exists():
        eda_dest = PROJECT_ROOT / "eda_plots"
        if eda_dest.exists():
            shutil.rmtree(eda_dest)
        shutil.copytree(eda_src, eda_dest)
        print(f"  eda_plots/ -> {eda_dest}")

    # --- streamlit manifest (path lama dari Kaggle, dipakai hanya sebagai referensi) ---
    manifest_src = tmp / "streamlit_manifest.json"
    if manifest_src.exists():
        shutil.copy2(manifest_src, PROJECT_ROOT / "streamlit_manifest_kaggle.json")
        print(f"  streamlit_manifest.json (referensi path Kaggle asli) -> "
              f"{PROJECT_ROOT / 'streamlit_manifest_kaggle.json'}")

    # tulis manifest LOKAL yang path-nya sudah menunjuk ke lokasi lokal
    local_manifest = {
        "detector_weights": str(WEBAPP_DIR / "runs" / "detect" / "pill_detector" / "weights" / "best.pt"),
        "classifier_weights": str(WEBAPP_DIR / "runs" / "classify_final" / "best.pt") if cls_src.exists() else None,
        "classifier_classes_json": str(WEBAPP_DIR / "runs" / "classify_final" / "class_names.json") if cls_classes_src.exists() else None,
        "detector_metrics": str(PROJECT_ROOT / "detector_metrics.json"),
        "journal_experiments_dir": str(PROJECT_ROOT / "journal_experiments"),
    }
    (PROJECT_ROOT / "streamlit_manifest.json").write_text(json.dumps(local_manifest, indent=2))
    print(f"  streamlit_manifest.json (path LOKAL, dipakai website) -> {PROJECT_ROOT / 'streamlit_manifest.json'}")

    shutil.rmtree(tmp)


def setup_test_package(zip_path: Path):
    print(f"\n[2] Menyiapkan test package dari {zip_path.name} ...")
    dest_dir = PROJECT_ROOT / "data" / "test_package"
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    extract_zip(zip_path, dest_dir)

    photos_dir = dest_dir / "photos"
    manifest_path = dest_dir / "manifest.json"
    n_photos = len(list(photos_dir.glob("*"))) if photos_dir.exists() else 0
    print(f"  Foto test: {n_photos} file di {photos_dir}")
    print(f"  Manifest : {manifest_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--research-zip", type=Path, default=None,
                     help="Path ke research_package_journal.zip hasil unduhan Kaggle")
    ap.add_argument("--test-package-zip", type=Path, default=None,
                     help="Path ke test_package.zip hasil unduhan Kaggle")
    args = ap.parse_args()

    if not args.research_zip and not args.test_package_zip:
        raise SystemExit(
            "Isi minimal salah satu argumen: --research-zip atau --test-package-zip.\n"
            "Contoh: python setup_from_kaggle_package.py --research-zip ~/Downloads/research_package_journal.zip"
        )

    print("=" * 70)
    print("SETUP HASIL KAGGLE -> STRUKTUR LOKAL UNTUK STREAMLIT")
    print("=" * 70)

    if args.research_zip:
        if not args.research_zip.exists():
            raise SystemExit(f"File tidak ditemukan: {args.research_zip}")
        setup_research_package(args.research_zip)

    if args.test_package_zip:
        if not args.test_package_zip.exists():
            raise SystemExit(f"File tidak ditemukan: {args.test_package_zip}")
        setup_test_package(args.test_package_zip)

    print("\n" + "=" * 70)
    print("SELESAI. Jalankan website dengan:")
    print("  pip install -r webapp/requirements.txt")
    print("  streamlit run webapp/streamlit_app.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
