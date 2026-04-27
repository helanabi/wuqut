#!/usr/bin/env python3

import csv
import sys
from pathlib import Path

DATA = Path.home() / ".local" / "share" / "wuqut" / "data.csv"

def main():
    try:
        with DATA.open() as f:
            reader = csv.reader(f)
            headers = next(reader)
            values = next(reader)
    except (OSError, csv.Error) as e:
        print(f"wuqut: failed to read {DATA}\n{e}", file=sys.stderr)
        sys.exit(1)
    
    label_width = max(len(h) for h in headers)
    value_width = max(len(v) for v in values)
    
    for h, v in zip(headers, values):
        print(f"{h:<{label_width}}  {v:>{value_width}}")
