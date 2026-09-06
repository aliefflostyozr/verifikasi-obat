"""Pencocokan hasil deteksi dengan e-resep (BAB IV.3 proposal)."""
from dataclasses import dataclass, field
import config


@dataclass
class DetectedItem:
    class_name: str
    count: int
    avg_confidence: float


@dataclass
class MatchResult:
    status: str
    detail_per_obat: list = field(default_factory=list)
    catatan: str = ""


def match_eresep(detected_items, eresep_items, low_conf_threshold=None):
    if low_conf_threshold is None:
        low_conf_threshold = config.CLASSIFIER_CONF_THRESHOLD
    if not eresep_items:
        return MatchResult(status=config.STATUS_GANGGUAN,
                            catatan="Data e-resep kosong/tidak dapat diakses.")
    detected_map = {d.class_name: d for d in detected_items}
    eresep_map = {e["nama_obat"]: e["jumlah"] for e in eresep_items}
    detail, ada_tidak_sesuai, ada_tidak_yakin = [], False, False
    for nama_obat in sorted(set(detected_map) | set(eresep_map)):
        jumlah_resep = eresep_map.get(nama_obat, 0)
        det = detected_map.get(nama_obat)
        jumlah_terdeteksi = det.count if det else 0
        confidence = det.avg_confidence if det else None
        cocok_jumlah = abs(jumlah_terdeteksi - jumlah_resep) <= config.QUANTITY_TOLERANCE
        if confidence is not None and confidence < low_conf_threshold:
            status_i, ada_tidak_yakin = config.STATUS_TIDAK_YAKIN, True
        elif nama_obat not in eresep_map or nama_obat not in detected_map or not cocok_jumlah:
            status_i, ada_tidak_sesuai = config.STATUS_TIDAK_SESUAI, True
        else:
            status_i = config.STATUS_SESUAI
        detail.append({"nama_obat": nama_obat, "jumlah_resep": jumlah_resep,
                        "jumlah_terdeteksi": jumlah_terdeteksi, "confidence": confidence,
                        "status": status_i})
    if ada_tidak_yakin:
        overall, catatan = config.STATUS_TIDAK_YAKIN, "Ada item confidence rendah -> verifikasi manual."
    elif ada_tidak_sesuai:
        overall, catatan = config.STATUS_TIDAK_SESUAI, "Ditemukan ketidaksesuaian jenis/jumlah."
    else:
        overall, catatan = config.STATUS_SESUAI, "Sesuai e-resep."
    return MatchResult(status=overall, detail_per_obat=detail, catatan=catatan)
