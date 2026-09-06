"""Pipeline end-to-end: 1 foto -> status verifikasi."""
import argparse, json, time
from collections import defaultdict
from pathlib import Path
import cv2
import numpy as np
import config
from eresep_matcher import DetectedItem, match_eresep
from visualize import draw_detections


class PillVerificationPipeline:
    def __init__(self, detector_weights, classifier_weights=None,
                 classifier_classes_json=None, device=None, classifier_model_name="mobilenet_v3_small"):
        from ultralytics import YOLO
        self.detector = YOLO(detector_weights)
        self.device = device
        self.classifier = None
        self.classifier_classes = None
        self.classifier_model_name = classifier_model_name
        if classifier_weights:
            self._load_classifier(classifier_weights, classifier_classes_json)

    def _build_classifier_arch(self, num_classes):
        import torch
        from torchvision import models
        name = self.classifier_model_name
        if name == "mobilenet_v3_small":
            m = models.mobilenet_v3_small()
            m.classifier[-1] = torch.nn.Linear(m.classifier[-1].in_features, num_classes)
        elif name == "efficientnet_b0":
            m = models.efficientnet_b0()
            m.classifier[-1] = torch.nn.Linear(m.classifier[-1].in_features, num_classes)
        elif name == "resnet50":
            m = models.resnet50()
            m.fc = torch.nn.Linear(m.fc.in_features, num_classes)
        elif name == "densenet121":
            m = models.densenet121()
            m.classifier = torch.nn.Linear(m.classifier.in_features, num_classes)
        else:
            raise ValueError(f"Arsitektur classifier tidak dikenal: {name}")
        return m

    def _load_classifier(self, weights_path, classes_json):
        import torch
        from torchvision import transforms
        classes_json = classes_json or str(Path(weights_path).parent / "class_names.json")
        self.classifier_classes = json.loads(Path(classes_json).read_text())
        model = self._build_classifier_arch(len(self.classifier_classes))
        model.load_state_dict(torch.load(weights_path, map_location="cpu"))
        model.eval()
        self.classifier = model
        self._cls_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((config.CLASSIFIER_IMG_SIZE, config.CLASSIFIER_IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def _classify_crop(self, crop_bgr):
        import torch
        crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
        x = self._cls_transform(crop_rgb).unsqueeze(0)
        with torch.no_grad():
            probs = torch.softmax(self.classifier(x), dim=1)[0]
            conf, idx = torch.max(probs, dim=0)
        return self.classifier_classes[idx.item()], float(conf.item())

    def run(self, image_path, timing=False):
        t_start = time.time()
        image = cv2.imread(str(image_path)) if isinstance(image_path, (str, Path)) else image_path
        if image is None:
            raise FileNotFoundError(f"Tidak bisa membaca gambar: {image_path}")
        t_read = time.time()

        det_result = self.detector.predict(source=image, conf=config.DETECTOR_CONF_THRESHOLD,
                                            iou=config.DETECTOR_IOU_THRESHOLD, device=self.device,
                                            verbose=False)[0]
        t_detect = time.time()

        boxes, labels, confidences = [], [], []
        for box in det_result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            det_conf = float(box.conf[0])
            boxes.append((x1, y1, x2, y2))
            if self.classifier is not None:
                crop = image[int(y1):int(y2), int(x1):int(x2)]
                if crop.size == 0:
                    labels.append("unknown"); confidences.append(0.0); continue
                cls_name, cls_conf = self._classify_crop(crop)
                labels.append(cls_name)
                confidences.append(min(det_conf, cls_conf))
            else:
                cls_id = int(box.cls[0])
                labels.append(self.detector.names.get(cls_id, str(cls_id)))
                confidences.append(det_conf)
        t_classify = time.time()

        aggregated = self._aggregate(labels, confidences)
        result = {"image": image, "boxes": boxes, "labels": labels,
                  "confidences": confidences, "aggregated": aggregated}
        if timing:
            result["timing_ms"] = {
                "read": (t_read - t_start) * 1000,
                "detect": (t_detect - t_read) * 1000,
                "classify": (t_classify - t_detect) * 1000,
                "total": (t_classify - t_start) * 1000,
            }
        return result

    @staticmethod
    def _aggregate(labels, confidences):
        sums = defaultdict(lambda: [0, 0.0])
        for label, conf in zip(labels, confidences):
            sums[label][0] += 1; sums[label][1] += conf
        return [DetectedItem(class_name=n, count=c, avg_confidence=t / c) for n, (c, t) in sums.items()]

    def verify_against_eresep(self, image_path, eresep_items, timing=False):
        t0 = time.time()
        result = self.run(image_path, timing=timing)
        match = match_eresep(result["aggregated"], eresep_items)
        status_by_class = {d["nama_obat"]: d["status"] for d in match.detail_per_obat}
        box_status = [status_by_class.get(lbl, "TIDAK_YAKIN") for lbl in result["labels"]]
        annotated = draw_detections(result["image"], result["boxes"], result["labels"],
                                     result["confidences"], box_status)
        out = {"match": match, "annotated_image": annotated, "raw": result}
        if timing:
            out["total_pipeline_ms"] = (time.time() - t0) * 1000
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--detector", required=True)
    ap.add_argument("--classifier", default=None)
    ap.add_argument("--classifier-classes", default=None)
    ap.add_argument("--eresep", required=True)
    ap.add_argument("--out", default="hasil_verifikasi.jpg")
    ap.add_argument("--device", default=None)
    args = ap.parse_args()
    eresep_items = json.loads(Path(args.eresep).read_text())
    pipeline = PillVerificationPipeline(args.detector, args.classifier, args.classifier_classes, args.device)
    output = pipeline.verify_against_eresep(args.image, eresep_items)
    print(f"Status: {output['match'].status} | {output['match'].catatan}")
    cv2.imwrite(args.out, output["annotated_image"])


if __name__ == "__main__":
    main()
