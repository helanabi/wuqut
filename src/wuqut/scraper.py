#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import csv
import sys
import warnings
import requests
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from platformdirs import user_data_path

MONTHS = (
    "يناير",
    "فبراير",
    "مارس",
    "أبريل",
    "ماي",
    "يونيو",
    "يوليوز",
    "غشت",
    "شتنبر",
    "أكتوبر",
    "نونبر",
    "دجنبر"
)

DATA_DIR = user_data_path("wuqut", appauthor=False)
DATA_PATH = DATA_DIR / "data.csv"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--out", help="output file name")
    parser.add_argument("--insecure", action="store_true")
    return parser.parse_args()

def extract_row(html, day, month, include_header=True):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="horaire")
    months = tuple(map(lambda month: month.strip(),
                       table.select_one("td:nth-child(3)").text.split('/')))
    for m in months:
        if m not in MONTHS:
            print("Unrecoginzed month name:", m, file=sys.stderr)
            sys.exit(1)
    
    months = tuple(map(lambda m: MONTHS.index(m)+1, months))
    row = []
    for i, tr in enumerate(table.find_all("tr", recursive=False)):
        td_list = tr.find_all("td", recursive=False)
        if i==0 and include_header \
           or \
           (int(td_list[2].text) == day and
            (
                (month == months[0] and i <= day) or
                (month == months[1] and i > day)
            )):
            row.append(tuple((tag.text.strip() for tag in td_list)))
    return row

def write_file(filename, rows):
    if filename:
        data_path = Path(filename)
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data_path = DATA_PATH

    with data_path.open('w', newline='') as f:
        writer = csv.writer(f)    

        if len(rows) != 2:
            print("Unexpected table structure", file=sys.stderr)
            sys.exit(1)

        header, data =  rows
        writer.writerow(header)
        writer.writerow(data)    

def main():
    args = parse_args()

    warnings.filterwarnings("ignore", "Unverified HTTPS request")
    try:
        response = requests.get(args.url, verify=not args.insecure)
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if not response.ok:
        print("Server error:", response.status_code, file=sys.stderr)
        sys.exit(1)

    today = datetime.today()
    html = response.content.decode()

    try:
        write_file(args.out, extract_row(html, today.day, today.month))
    except OSError as e:
        print("Failed to write data\n{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
