"""Utility menggambar hasil deteksi+klasifikasi ke atas foto."""
import cv2
import numpy as np

STATUS_COLORS = {"SESUAI": (0, 165, 0), "TIDAK_SESUAI": (0, 0, 220), "TIDAK_YAKIN": (0, 165, 255)}


def draw_detections(image, boxes, labels, confidences, box_status=None):
    out = image.copy()
    for i, (x1, y1, x2, y2) in enumerate(boxes):
        status = box_status[i] if box_status else None
        color = STATUS_COLORS.get(status, (255, 200, 0))
        cv2.rectangle(out, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        text = f"{labels[i]} {confidences[i]:.2f}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(out, (int(x1), int(y1) - th - 6), (int(x1) + tw + 4, int(y1)), color, -1)
        cv2.putText(out, text, (int(x1) + 2, int(y1) - 4), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return out
