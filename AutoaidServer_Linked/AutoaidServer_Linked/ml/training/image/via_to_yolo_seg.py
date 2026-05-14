
"""Convert VIA polygon annotations to YOLOv8 segmentation format.

YOLOv8 segmentation label format:
<class_id> x1 y1 x2 y2 ... xn yn  (normalized)

This script:
- Reads VIA JSON (keyed by filename)
- Recursively searches for images if needed
- Writes YOLO images/labels splits + dataset.yaml + classes.json

Usage:
python via_to_yolo_seg.py --via_train 0Train_via_annos.json --via_val 0Val_via_annos.json --images_dir <dir> --out_dir <out>
"""

import argparse
import json
from pathlib import Path
import cv2


def load_via(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def normalize_poly(xs, ys, w, h):
    coords = []
    for x, y in zip(xs, ys):
        coords.append(x / w)
        coords.append(y / h)
    return coords


def convert_split(via_json: Path, images_dir: Path, out_images: Path, out_labels: Path, class_to_id: dict):
    ann = load_via(via_json)
    for img_name, data in ann.items():
        src = images_dir / img_name
        if not src.exists():
            matches = list(images_dir.rglob(img_name))
            if not matches:
                raise FileNotFoundError(f"Image not found: {img_name}")
            src = matches[0]

        img = cv2.imread(str(src))
        if img is None:
            raise RuntimeError(f"Failed reading image: {src}")
        h, w = img.shape[:2]

        (out_images / img_name).parent.mkdir(parents=True, exist_ok=True)
        (out_images / img_name).write_bytes(src.read_bytes())

        label_path = out_labels / (Path(img_name).stem + '.txt')
        lines = []
        for region in data.get('regions', []):
            cls = region.get('class')
            if cls is None:
                continue
            if cls not in class_to_id:
                class_to_id[cls] = len(class_to_id)
            cid = class_to_id[cls]
            xs = region.get('all_x', [])
            ys = region.get('all_y', [])
            if len(xs) < 3 or len(xs) != len(ys):
                continue
            coords = normalize_poly(xs, ys, w, h)
            lines.append(str(cid) + ' ' + ' '.join(f"{c:.6f}" for c in coords))

        label_path.parent.mkdir(parents=True, exist_ok=True)
        label_path.write_text('
'.join(lines) + ('
' if lines else ''), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--via_train', required=True)
    ap.add_argument('--via_val', required=True)
    ap.add_argument('--images_dir', required=True)
    ap.add_argument('--out_dir', required=True)
    args = ap.parse_args()

    images_dir = Path(args.images_dir)
    out_dir = Path(args.out_dir)

    out_images_train = out_dir / 'images' / 'train'
    out_images_val = out_dir / 'images' / 'val'
    out_labels_train = out_dir / 'labels' / 'train'
    out_labels_val = out_dir / 'labels' / 'val'

    for p in [out_images_train, out_images_val, out_labels_train, out_labels_val]:
        p.mkdir(parents=True, exist_ok=True)

    class_to_id = {}
    convert_split(Path(args.via_train), images_dir, out_images_train, out_labels_train, class_to_id)
    convert_split(Path(args.via_val), images_dir, out_images_val, out_labels_val, class_to_id)

    names = [None] * len(class_to_id)
    for k, v in class_to_id.items():
        names[v] = k

    (out_dir / 'classes.json').write_text(json.dumps(class_to_id, indent=2), encoding='utf-8')

    yaml = f"""# Auto-generated YOLOv8 dataset config
path: {out_dir.as_posix()}
train: images/train
val: images/val

names:
"""
    for i, name in enumerate(names):
        yaml += f"  {i}: {name}
"

    (out_dir / 'dataset.yaml').write_text(yaml, encoding='utf-8')
    print('Done. Classes:', class_to_id)


if __name__ == '__main__':
    main()
