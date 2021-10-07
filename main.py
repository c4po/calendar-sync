from datetime import datetime, timedelta, date
from google_calendar import GoogleCalendar
from outlook_client import OutlookCalendar
import configparser
import pytz


def main():
    configParser = configparser.ConfigParser()
    configFile = r'config.txt'
    configParser.read(configFile)
    OutlookCalendarPrefix = "=["+configParser.get('Outlook', 'prefix')+"]="
    GoogleCalendarPrefix = "=["+configParser.get('Google', 'prefix')+"]="
    CalendarSyncDays = 2

    googleCalendar = GoogleCalendar()
    outlookCalendar = OutlookCalendar()

    checkBegin = datetime.now(pytz.timezone(
        'America/Toronto')).replace(hour=0, minute=0, second=0, microsecond=0)
    checkEnd = checkBegin+timedelta(days=CalendarSyncDays)

    allGoogleEvents = googleCalendar.get_google_calendar(
        checkBegin.isoformat(), checkEnd.isoformat(), GoogleCalendarPrefix)
    allOutlookEvents = outlookCalendar.get_outlook_calendar(
        checkBegin, checkEnd, OutlookCalendarPrefix)

    outlookGoogleEvents = list(
        filter(lambda x: x.hasPrefix(OutlookCalendarPrefix), allGoogleEvents))
    originGoogleEvents = list(
        filter(lambda x: not x.hasPrefix(OutlookCalendarPrefix), allGoogleEvents))
    googleOutlookEvents = list(
        filter(lambda x: x.hasPrefix(GoogleCalendarPrefix), allOutlookEvents))
    originOutlookEvents = list(
        filter(lambda x: not x.hasPrefix(GoogleCalendarPrefix), allOutlookEvents))

    setOutlookGoogleEvents = set((event.start, event.end, event.summary)
                          for event in outlookGoogleEvents)
    newGoogleEvents = [event for event in originOutlookEvents if (
        event.start, event.end, event.summary) not in setOutlookGoogleEvents]
    setOriginOutlookEvents = set((event.start, event.end, event.summary)
                          for event in originOutlookEvents)
    delGoogleEvents = [event for event in outlookGoogleEvents if (
        event.start, event.end, event.summary) not in setOriginOutlookEvents]
    
    setOutlookEvents = set((event.start, event.end, event.summary)
                           for event in googleOutlookEvents)
    newOutlookEvents = [event for event in originGoogleEvents if (
        event.start, event.end, event.summary) not in setOutlookEvents]

    print("========================outlookGoogleEvents")
    for event in outlookGoogleEvents:
        print(event.start, event.end, event.summary)
    print("========================originGoogleEvents")
    for event in originGoogleEvents:
        print(event.start, event.end, event.summary)

    print("========================googleOutlookEvents")
    for event in googleOutlookEvents:
        print(event.start, event.end, event.summary)
    print("========================originOutlookEvents")
    for event in originOutlookEvents:
        print(event.start, event.end, event.summary)


    print("========================newGoogleEvents")
    for event in newGoogleEvents:
        print(event.start, event.end, event.summary)
        # googleCalendar.create_google_event(event)
    print("========================delGoogleEvents")
    for event in delGoogleEvents:
        print(event.start, event.end, event.summary)
        # googleCalendar.delete_google_event(event)


    print("========================newOutlookEvents")
    for event in newOutlookEvents:
        print(event.start, event.end, event.summary)
        # outlookCalendar.create_outlook_event(event)


if __name__ == '__main__':

    main()
