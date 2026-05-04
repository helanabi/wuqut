#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
from datetime import datetime
from . import scrape
from .prayer import Prayer

def parse_args():
    parser = argparse.ArgumentParser(
        prog="wuqut",
        description="Extract Moroccan prayer times from the official source"
    )

    megrp = parser.add_mutually_exclusive_group()
    megrp.add_argument("-r", "--raw", action="store_true",
                       help="print raw values for the current day")
    return parser.parse_args()

def fprint(headers, values):
    """Format and print a sequence of headers and values."""
    
    label_width = max(len(h) for h in headers)
    value_width = max(len(v) for v in values)
    
    for h, v in zip(headers, values):
        print(f"{h:<{label_width}}  {v:>{value_width}}")

def main():
    args = parse_args()
    now = datetime.now()
    info_today = scrape.get(now.date())

    if args.raw:
        fprint(*info_today)
        return

    labels = ("Fajr", "Shuruq", "Duhr", "Asr", "Maghreb", "Isha'")
    prayers = tuple(
        Prayer(val, label) for label, val in zip(labels, info_today[1][3:])
    )
    prev, _next = Prayer.adjacent(prayers, now)
    if not prev or abs(prev.delta(now)) > abs(_next.delta(now)):
        print(_next.delta(now, seconds=False))
    else:
        print(prev.delta(now, seconds=False))

if __name__ == "__main__":
    main()
