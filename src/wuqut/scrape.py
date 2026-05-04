# SPDX-License-Identifier: GPL-3.0-or-later

import datetime
import sys
from datetime import timedelta
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

def extract_row(html, day, month, include_header=True):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="horaire")
    months = tuple(map(lambda month: month.strip(),
                       table.select_one("td:nth-child(3)").text.split('/')))
    for m in months:
        if m not in MONTHS:
            print("Unrecoginzed month name:", m, file=sys.stderr)
            sys.exit(9)
    
    months = tuple(map(lambda m: MONTHS.index(m)+1, months))
    row = []
    for i, tr in enumerate(table.find_all("tr")):
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

def get(date):
    """Return a sequence of labels and values of a given date.

    date - datetime.date
    """
    for file in DATA_DIR.glob("????-??-??.html"):
        file_date = datetime.date.fromisoformat(file.name.split('.')[0])
        if timedelta() <= date - file_date <= timedelta(days=29):
            return extract_row(file.read_text(), date.day, date.month)

    print("No data file is available for the current month", file=sys.stderr)
    sys.exit(3)
