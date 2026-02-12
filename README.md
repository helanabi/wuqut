## Overview

Prayer times scraper from Moroccan government website

## Usage

```
usage: scrape-prayer-times.py [-h] [--out OUT] [--insecure] url

positional arguments:
  url

options:
  -h, --help  show this help message and exit
  --out OUT   output file name
  --insecure
```
## Project Status

This is a minimal MVP demonstrating HTML manipulation using `beautifulsoup4`.  
The tool currenly saves prayer times for the current day to a csv file  
defined by the option `--out` or `output.csv` by default.  
The plan is to use this script as a baseline for a more practical prayer  
times CLI application.