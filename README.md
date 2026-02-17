## Overview

Prayer times in Morocco from the official source on your terminal

## Project Status

This is a minimal MVP demonstrating HTML manipulation using `beautifulsoup4`.  
The tool currenly saves prayer times for the current day to a csv file  
defined by the option `--out` or `output.csv` by default.  
The plan is to use this script as a baseline for a more practical prayer  
times CLI application.

## Usage

```
usage: wuqut.py [-h] [--out OUT] [--insecure] url

positional arguments:
  url

options:
  -h, --help  show this help message and exit
  --out OUT   output file name
  --insecure
```

## Installation ##

- `wuqut.py`
The program still lives in a single Python script, install it on your system  
anyway you prefer (notice `requirements.txt`).

- `wuqut.service`
Optional **systemd service** configuration file, which assumes that the script  
is installed as `~/.local/bin/wuqut`, and saves data to  
`~/.local/share/wuqut/data.csv`. You may change these paths to your liking.

- `wuqut.timer`
Optional **systemd timer** configuration file, which runs the above service  
daily at 06:00 AM.