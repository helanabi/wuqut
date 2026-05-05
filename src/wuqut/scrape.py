# SPDX-License-Identifier: GPL-3.0-or-later

import datetime
import sys
import warnings
import requests
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
DATA_FILE = DATA_DIR / "page.html"
URL = "https://habous.gov.ma/prieres/horaire_hijri_2.php"

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
    if not DATA_FILE.exists():
        print("Data file is not found\n"
              "Use '--update' to download the file",
              file=sys.stderr)
        sys.exit(3)

    row = extract_row(DATA_FILE.read_text(), date.day, date.month)
    if not row:
        print("Data file is out-of-date\n"
              "Use '--update' to update the file",
              file=sys.stderr)
        sys.exit(4)
    return row

def update(city_id):
    warnings.filterwarnings("ignore", "Unverified HTTPS request")
    try:
        res = requests.get(URL, params={"ville": city_id}, verify=False)
    except requests.RequestException as e:
        print(f"Failed to connect to server\n{e}",
              file=sys.stderr)
        sys.exit(6)

    if not res.ok:
        print(f"Server responded with error code: {res.status_code}",
              file=sys.stderr)
        sys.exit(5)

    DATA_DIR.mkdir(exist_ok=True)
    DATA_FILE.write_text(res.text)
