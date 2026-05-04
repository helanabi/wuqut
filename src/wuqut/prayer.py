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

    def delta(self, ref_time, human_readable=False):
        diff = (ref_time - self.time).total_seconds()
        
        if not human_readable:
            return abs(diff)

        seconds = int(abs(diff))
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        hours_str = f"{hours}س"
        minutes_str = f"{minutes}د"
        seconds_str = f"{seconds}ث"

        if hours:
            time_str = hours_str + ' ' + minutes_str
        elif minutes:
            time_str = minutes_str
        else:
            time_str = seconds_str

        if diff < 0:
            return "بقي " + time_str + " على " + self.label
        else:
            return "مرّ " + time_str + " على " + self.label
