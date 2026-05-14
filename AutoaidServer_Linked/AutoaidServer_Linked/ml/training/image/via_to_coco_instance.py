
"""Convert VIA polygon annotations to COCO instance segmentation.

Usage:
python via_to_coco_instance.py --via 0Train_via_annos.json --images_dir <dir> --out coco_train.json
"""

import argparse
import json
from pathlib import Path

import cv2
from shapely.geometry import Polygon


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--via', required=True)
    ap.add_argument('--images_dir', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    via = json.loads(Path(args.via).read_text(encoding='utf-8'))
    images_dir = Path(args.images_dir)

    categories = {}
    images = []
    annotations = []

    ann_id = 1
    img_id = 1

    for img_name, data in via.items():
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

        images.append({'id': img_id, 'file_name': img_name, 'width': w, 'height': h})

        for region in data.get('regions', []):
            cls = region.get('class')
            if cls is None:
                continue
            if cls not in categories:
                categories[cls] = len(categories) + 1
            cat_id = categories[cls]

            xs = region.get('all_x', [])
            ys = region.get('all_y', [])
            if len(xs) < 3 or len(xs) != len(ys):
                continue

            poly = [(float(x), float(y)) for x, y in zip(xs, ys)]
            pg = Polygon(poly)
            if not pg.is_valid:
                pg = pg.buffer(0)
            area = float(pg.area)
            minx, miny, maxx, maxy = pg.bounds
            bbox = [float(minx), float(miny), float(maxx - minx), float(maxy - miny)]
            segmentation = [sum(([x, y] for x, y in poly), [])]

            annotations.append({
                'id': ann_id,
                'image_id': img_id,
                'category_id': cat_id,
                'segmentation': segmentation,
                'area': area,
                'bbox': bbox,
                'iscrowd': 0,
            })
            ann_id += 1

        img_id += 1

    coco = {
        'info': {'description': 'AutoAid VIA->COCO', 'version': '1.0'},
        'licenses': [],
        'images': images,
        'annotations': annotations,
        'categories': [{'id': v, 'name': k} for k, v in categories.items()],
    }

    Path(args.out).write_text(json.dumps(coco, indent=2), encoding='utf-8')
    print('Done. Categories:', categories)


if __name__ == '__main__':
    main()
