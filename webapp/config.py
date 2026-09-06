"""Konfigurasi terpusat sistem verifikasi obat."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
RUNS_DIR = ROOT_DIR / "runs"
EDA_DIR = ROOT_DIR / "eda"

DETECTOR_MODEL_NAME = "yolov8n.pt"
DETECTOR_IMG_SIZE = 640
DETECTOR_CONF_THRESHOLD = 0.35
DETECTOR_IOU_THRESHOLD = 0.45

CLASSIFIER_MODEL_NAME = "mobilenet_v3_small"
CLASSIFIER_IMG_SIZE = 128
CLASSIFIER_CONF_THRESHOLD = 0.55

QUANTITY_TOLERANCE = 0

STATUS_SESUAI = "SESUAI"
STATUS_TIDAK_SESUAI = "TIDAK_SESUAI"
STATUS_TIDAK_YAKIN = "TIDAK_YAKIN"
STATUS_GANGGUAN = "GANGGUAN_DATA"

RANDOM_SEED = 42

# Arsitektur yang dibandingkan (bagian 1: baseline/SOTA comparison)
DETECTOR_BASELINE_MODELS = ["yolov8n.pt", "yolov5nu.pt", "yolo11n.pt"]  # + faster-rcnn (terpisah)
CLASSIFIER_BASELINE_MODELS = ["mobilenet_v3_small", "efficientnet_b0", "resnet50", "densenet121"]
