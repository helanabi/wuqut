#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import csv
import sys
from datetime import datetime
from platformdirs import user_data_path

DATA = user_data_path("wuqut", appauthor=False) / "data.csv"

def parse_args():
    parser = argparse.ArgumentParser(prog="wuqut",
                                     description="Pretty-print prayer times")
    parser.add_argument("-d", "--day", action="store_true",
                        help="Print today's prayer times")
    parser.add_argument("-n", "--next", action="store_true",
                        help="Print next prayer and time left")
    return parser.parse_args()

def fprint(headers, values):
    """Format and print a sequence of headers and values."""
    
    label_width = max(len(h) for h in headers)
    value_width = max(len(v) for v in values)
    
    for h, v in zip(headers, values):
        print(f"{h:<{label_width}}  {v:>{value_width}}")
        
# todo: implement flags: --next, --previous, default: auto
def main():
    try:
        with DATA.open() as f:
            reader = csv.reader(f)
            headers = next(reader)
            values = next(reader)
    except (OSError, csv.Error) as e:
        print(f"wuqut: failed to read {DATA}\n{e}", file=sys.stderr)
        sys.exit(1)

    args = parse_args()

    if args.day:
        fprint(headers, values)
        return


if __name__ == "__main__":
    main()
