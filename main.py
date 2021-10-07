from datetime import datetime, timedelta
from google_calendar import GoogleCalendar
from outlook_client import OutlookCalendar

OutlookCalendarPrefix="=[CPPIB]="
GoogleCalendarPrefix="=[Google]="
CalendarSyncDays=2

def main():
    googleCalendar = GoogleCalendar()
    outlookCalendar = OutlookCalendar()

    print('Getting list of calendars')
    googleCheckBegin = datetime.utcnow()-timedelta(days=1)
    allGoogleEvents = googleCalendar.get_google_calendar(googleCheckBegin.isoformat()+'Z',10, GoogleCalendarPrefix)
    outlookGoogleEvents = list(filter(lambda x: x.hasPrefix(OutlookCalendarPrefix), allGoogleEvents))
    originGoogleEvents = list(filter(lambda x: not x.hasPrefix(OutlookCalendarPrefix), allGoogleEvents))
    print("========================outlookGoogleEvents")
    for event in outlookGoogleEvents:
        print (event.start, event.end, event.summary)
    print("========================originGoogleEvents")
    for event in originGoogleEvents:
        print (event.start, event.end, event.summary)

    print("========================")
    checkbegin = datetime.now()
    checkend = checkbegin + timedelta(days=CalendarSyncDays)
    allOutlookEvents = outlookCalendar.get_outlook_calendar(checkbegin, checkend, OutlookCalendarPrefix)
    googleOutlookEvents =  list(filter(lambda x: x.hasPrefix(GoogleCalendarPrefix), allOutlookEvents))
    originOutlookEvents =  list(filter(lambda x: not x.hasPrefix(GoogleCalendarPrefix), allOutlookEvents))
    print("========================googleOutlookEvents")
    for event in googleOutlookEvents:
        print (event.start, event.end, event.summary)
    print("========================originOutlookEvents")
    for event in originOutlookEvents:
        print (event.start, event.end, event.summary)


    setGoogleEvents=set((event.start, event.end, event.summary) for event in outlookGoogleEvents)
    newGoogleEvents = [event for event in originOutlookEvents if (event.start, event.end, event.summary) not in setGoogleEvents]
    print("========================newGoogleEvents")
    for event in newGoogleEvents:
        print (event.start, event.end, event.summary)
        # googleCalendar.create_google_event(event)

    setOutlookEvents=set((event.start, event.end, event.summary) for event in googleOutlookEvents)
    newOutlookEvents = [event for event in originGoogleEvents if (event.start, event.end, event.summary) not in setOutlookEvents]
    print("========================newOutlookEvents")
    for event in newOutlookEvents:
        print (event.start, event.end, event.summary)
        # outlookCalendar.create_outlook_event(event.start, 30, event.summary, event.description)

if __name__ == '__main__':
    main()
