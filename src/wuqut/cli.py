#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import sys
import requests

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
    megrp.add_argument("-u", "--update", action="store_true",
                       help="update local files")
    megrp.add_argument("-f", "--force-utc", action="store_true",
                       help="assume system time is set to UTC when Daylight "
                       "Saving Time is in effect")
    parser.add_argument("-c", "--city-id", type=int, metavar="ID",
                        help="Only useful with '--update'. Ignored otherwise")
    return parser.parse_args()

def fprint(headers, values):
    """Format and print a sequence of headers and values."""
    
    label_width = max(len(h) for h in headers)
    value_width = max(len(v) for v in values)
    
    for h, v in zip(headers, values):
        print(f"{h:<{label_width}}  {v:>{value_width}}")

def main():
    args = parse_args()

    if args.update:
        if not args.city_id:
            print("Error: Missing option: -c/--city-id", file=sys.stderr)
            sys.exit(2)
        scrape.update(args.city_id)
        return
    
    now = datetime.now()
    info_today = scrape.get(now.date())

    if args.raw:
        fprint(*info_today)
        return

    labels = ("Fajr", "Shuruq", "Duhr", "Asr", "Maghreb", "Isha'")
    prayers = tuple(
        Prayer(val, label) for label, val in zip(labels, info_today[1][3:])
    )

    if args.force_utc:
        for prayer in prayers:
            prayer.undo_dst()

    prev, _next = Prayer.adjacent(prayers, now)
    if not prev or _next and prev.delta(now) > _next.delta(now):
        print(_next.delta(now, seconds=False))
    else:
        print(prev.delta(now, seconds=False))

if __name__ == "__main__":
    main()
