'''module with model definitions for lst'''

import time

from datetime import datetime, tzinfo, timedelta

class TzInfo(tzinfo):
    '''class to support timezones in datetime'''
    def utcoffset(self, dt):
        return timedelta(seconds=time.timezone)

    def dst(self, dt):
        return timedelta(seconds=time.altzone)

    def tzname(self, dt):
        return time.tzname[0] if not time.daylight else time.tzname[1]

class List(object):
    '''an object representing a complete list'''

    def __init__(self, name, handle):
        self.name = name
        self.handle = handle

    def add_line(self, line):
        '''add a line to the list file'''
        self.handle.write(str(line))
        self.handle.write('\n')

    def __iter__(self):
        for line in self.handle:
            yield ListItem.from_string(line)

    def __getitem__(self, val):
        index = 0

        for i in range(val.start, val.stop, val.step):
            if i % val.step == 0:
                line = self.handle.readline()
                yield (i, ListItem.from_string(line))
            else:
                self.handle.readline()

    @classmethod
    def from_path(cls, name, path, for_writing=False):
        '''create a List object from a path'''
        mode = 'a' if for_writing else 'r'
        return cls(name, open(path, mode))

class ListItem(object):
    '''an object represeting a list item'''

    FORMAT = "{status} {date} {msg}{tagsep}{tags}"
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%Z"
    HUMAN_DATE_FORMAT = "%c"

    def __init__(self, msg, tags=None, active=True, time=None, msg_format=FORMAT,
            date_format=DATE_FORMAT, active_icon="*", removed_icon="x"):
        self.msg = msg
        self.tags = tags if tags is not None else []
        self.active = active
        self.time = time if time is not None else datetime.now(TzInfo())

        self.msg_format = msg_format
        self.date_format = date_format
        self.active_icon = active_icon
        self.removed_icon = removed_icon

    def __str__(self):
        '''return a string representation of the item'''
        status = self.active_icon if self.active else self.removed_icon
        date = self.time.strftime(self.date_format)
        tags = " ".join(self.tags)
        tagsep = " # " if self.tags else ""

        return self.msg_format.format(status=status, date=date, msg=self.msg,
                tagsep=tagsep, tags=tags)

    def to_string(self, prefix=""):
        '''return a more human readable representation of the item'''
        status = self.active_icon if self.active else self.removed_icon
        date = self.time.strftime(self.HUMAN_DATE_FORMAT)
        tags = " ".join(self.tags)
        tagsep = " # " if self.tags else ""

        return prefix + self.msg_format.format(status=status, date=date,
                msg=self.msg, tagsep=tagsep, tags=tags)


    @classmethod
    def from_string(cls, line, date_format=DATE_FORMAT, active_icon="*",
            removed_icon="x"):
        '''return a ListItem instance from a line'''
        line = line.strip()
        parts = line.split()

        icon = parts[0]
        date = parts[1]

        msg_and_tags = [item.strip() for item in line.split(" ", 2)[2].split("#", 1)]

        msg = msg_and_tags[0]

        if len(msg_and_tags) == 1:
            tags = ""
        else:
            tags = msg_and_tags[1]

        active = True if icon == active_icon else False

        date_parts = list(time.strptime(date, date_format)[0:6])
        date_parts.append(0)
        date_parts.append(TzInfo())
        parsed_date = datetime(*date_parts)

        return cls(msg, tags.split(), active, parsed_date, cls.FORMAT,
                date_format, active_icon, removed_icon)

