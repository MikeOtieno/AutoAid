
"""Create a CSV manifest for audio classification.

Leaf directory name becomes the label.
Output CSV columns: path,label
"""

import argparse
from pathlib import Path
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root_dir', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    root = Path(args.root_dir)
    rows = []
    for wav in root.rglob('*.wav'):
        rows.append({'path': str(wav.resolve()), 'label': wav.parent.name})

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")


if __name__ == '__main__':
    main()
