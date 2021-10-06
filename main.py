from datetime import datetime, timedelta
from google_calendar import GoogleCalendar
from outlook_client import OutlookCalendar

CalendarPrefix="[CPPIB]"
CalendarSyncDays=10

def main():
    googleCalendar = GoogleCalendar()
    outlookCalendar = OutlookCalendar()

    print('Getting list of calendars')
    googleCheckBegin = datetime.utcnow()-timedelta(days=1)
    googleEvents = googleCalendar.get_google_calendar(googleCheckBegin.isoformat()+'Z',100,CalendarPrefix)
    # for event in googleEvents:
    #     print (event.start, event.end, event.summary)
    # print("========================")

    checkbegin = datetime.now()
    checkend = checkbegin + timedelta(days=CalendarSyncDays)
    outlookEvents = outlookCalendar.get_outlook_calendar(checkbegin, checkend, CalendarPrefix)
    # for event in outlookEvents:
    #     print (event.start, event.end, event.summary)


    setGoogleEvents=set((event.start, event.end, event.summary) for event in googleEvents)
    newEvents = [event for event in outlookEvents if (event.start, event.end, event.summary) not in setGoogleEvents]
    for event in newEvents:
        print (event.start, event.end, event.summary)
        googleCalendar.create_google_event(event)


    googleEvents = googleCalendar.get_google_calendar(googleCheckBegin.isoformat()+'Z',100)
    newGoogleEvents = [event for event in googleEvents if not event.summary.startswith(CalendarPrefix)]

    for event in newGoogleEvents:
        outlookCalendar.create_outlook_event(event.start, 30, event.summary, event.description)

if __name__ == '__main__':
    main()
