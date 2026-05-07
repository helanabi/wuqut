## Overview

**Wuqut** is a CLI tool for extracting prayer times from the Moroccan Ministry of Habous website.

![wuqut demo](demo.gif)

## Features

- By default, it displays time left until the next prayer or elapsed time since the last prayer depending on which is closest
- Optionally displays raw current day values (including Hijri date)
- Requires internet connection only once a month to update local data
- Optionally converts to UTC time for users opting out of Daylight Saving Time

## Usage

```
usage: wuqut [-h] [-r | -u | -t] [-c ID]

Extract Moroccan prayer times from the official source

options:
  -h, --help        show this help message and exit
  -r, --raw         print raw values for the current day
  -u, --update      update local files
  -t, --force-utc   assume system time is set to UTC when Daylight Saving Time
                    is in effect
  -c, --city-id ID  Only useful with '--update'. Ignored otherwise
```

## Requirements

Python 3.10+

## Installation

* `pip install git+https://github.com/helanabi/wuqut.git@v0.3.0`

> Use `pipx` for user-level installation (doesn't require root access)  

## Configuration

* GNU/Linux users using systemd as their init system can use the example service/timer configuration files to auto-update data. For example:
  - `cp wuqut.service wuqut.timer ~/.config/systemd/user/`
  - `systemctl --user enable wuqut.timer`

> If you don't know what your init system is, you most likely are using systemd  
> To confirm, run: `ps c -ocmd= 1`

* Set the '--city-id' option to match your city ID.  If you don't know what your city ID is, visit [upstream URL](https://habous.gov.ma/prieres/horaire_hijri_2.php?ville=3), use the dropdown box to select your city, the URL will change to reflect your city's ID.

## Exit Codes

- `1`: operating system error
- `2`: usage error
- `3`: data unavailable
- `4`: data out-of-date
- `5`: server error
- `6`: network error
- `9`: unexpected error

## LICENSE

This project is licensed under the GNU General Public License v3.0 or later.  
See the COPYING file for details.
