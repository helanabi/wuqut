#!/usr/bin/env python

import argparse
import csv
import sys
import warnings
import requests
from datetime import datetime
from bs4 import BeautifulSoup

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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--out", default="output.csv", help="output file name")
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

def main():
    args = parse_args()

    warnings.filterwarnings("ignore", "Unverified HTTPS request")
    try:
        response = requests.get(args.url, verify=not args.insecure)
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        sys.exit(3)

    if not response.ok:
        print("Server error:", response.status_code, file=sys.stderr)
        sys.exit(2)

    today = datetime.today()
    with open(args.out, 'w', newline='') as f:
        writer = csv.writer(f)
        html = response.content.decode()
        rows = extract_row(html, today.day, today.month)

        if len(rows) != 2:
            print("Unexpected table structure", file=sys.stderr)
            sys.exit(1)

        header, data =  rows
        writer.writerow(header)
        writer.writerow(data)
