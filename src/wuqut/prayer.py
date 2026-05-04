# SPDX-License-Identifier: GPL-3.0-or-later

import datetime

class Prayer:
    # Static methods
    def adjacent(prayers, ref_time):
        if ref_time < prayers[0].time:
            return None, prayers[0]

        for i in range(len(prayers[:-1])):
            if prayers[i].time < ref_time < prayers[i+1].time:
                return prayers[i], prayers[i+1]

        return prayers[-1], None

    # Instance methods
    def __init__(self, time_str, label, date=datetime.date.today()):
        self.label = label
        time = map(int, time_str.split(':'))
        self.time = datetime.datetime(year=date.year,
                                      month=date.month,
                                      day=date.day,
                                      hour=next(time),
                                      minute=next(time))

    def delta(self, ref_time, seconds=True):
        diff = (ref_time - self.time).total_seconds()
        negative = diff < 0
        diff = abs(diff)
        
        if seconds:
            return diff

        seconds = int(diff)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        hours_str = f"{hours}h"
        minutes_str = f"{minutes}m"
        seconds_str = f"{seconds}s"

        if hours:
            time_str = hours_str + ' ' + minutes_str
        elif minutes:
            time_str = minutes_str
        else:
            time_str = seconds_str

        if negative:
            time_str = '-' + time_str

        return self.label + ": " + time_str

    def undo_dst(self):
        """Undo Daylight Saving Time."""
        self.time = self.time - datetime.timedelta(hours=1)
