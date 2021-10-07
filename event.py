from datetime import datetime, timedelta
import pytz
import re

regPrefix = r"^\=\[\w+\]\="


class Event:
    def __init__(self, start, end, summary, description, eventid):
        self.start = start
        self.end = end
        self.summary = summary
        self.description = description
        self.eventid = eventid

    @classmethod
    def googleEvent(cls, event, prefix):
        if event['start'].get('dateTime'):
            start = datetime.strptime(event['start'].get(
                'dateTime'), '%Y-%m-%dT%H:%M:%S%z')
        else:
            start = datetime.strptime(event['start'].get('date'), '%Y-%m-%d')
        if event['end'].get('dateTime'):
            end = datetime.strptime(event['end'].get(
                'dateTime'), '%Y-%m-%dT%H:%M:%S%z')
        else:
            end = datetime.strptime(event['end'].get('date'), '%Y-%m-%d')
        if re.match(regPrefix, event['summary']):
            summary = event['summary']
        else:
            summary = prefix + event['summary']
        description = event.get('description', "")
        eventid = event['id']
        e = cls(start, end, summary, description, eventid)
        return e

    @classmethod
    def outlookEvent(cls, event, prefix):
        start = datetime.fromtimestamp(timestamp=event.start.timestamp(
        ), tz=pytz.timezone('America/Toronto'))+timedelta(hours=4)
        end = datetime.fromtimestamp(timestamp=event.end.timestamp(
        ), tz=pytz.timezone('America/Toronto'))+timedelta(hours=4)
        if re.match(regPrefix, event.subject):
            summary = event.subject
        else:
            summary = prefix + event.subject
        description = event.body
        e = cls(start, end, summary, description, "")
        return e

    def hasPrefix(self, prefix):
        return self.summary.startswith(prefix)
