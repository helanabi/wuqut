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
    return parser.parse_args()

def main():
    args = parse_args()
    now = datetime.now()
    info_today = scrape.get(now.date())
    prayers = tuple(Prayer(val, label) for label, val in info_today[3:])
    prev, _next = Prayer.adjacent(prayers, now)
    if not prev or prev.delta(now) > _next.delta(now):
        print(_next.delta(now, human_readable=True))
    else:
        print(prev.delta(now, human_readable=True))

if __name__ == "__main__":
    main()
