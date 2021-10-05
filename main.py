from datetime import datetime, timedelta
from google_calendar import GoogleCalendar
from outlook_client import get_outlook_calendar, create_outlook_event

def main():
    googleCalendar = GoogleCalendar()
    print('Getting list of calendars')
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    googleCalendar.get_google_calendar(now,10,"Lucas")


    today = datetime.now().date()
    event_start = datetime(today.year, today.month, today.day, 10, 30)+timedelta(days=2)
    googleCalendar.create_google_event(event_start, 30, "[CPPIB] test", "test description")
    # today = datetime.now().date()
    # tomorrow = datetime(today.year, today.month, today.day, 10)+timedelta(days=1)
    # start = tomorrow.isoformat()
    # end = (tomorrow + timedelta(hours=1)).isoformat()
    # event_result = service.events().insert(calendarId='primary',
    #    body={
    #        "summary": 'Automating calendar',
    #        "description": 'This is a tutorial example of automating google calendar with python',
    #        "start": {"dateTime": start, "timeZone": 'America/Toronto'},
    #        "end": {"dateTime": end, "timeZone": 'America/Toronto'},
    #    }
    # ).execute()

    # Call the Calendar API
    # print('Getting list of calendars')
    # now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # calendars_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=50, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = calendars_result.get('items', [])
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     end = event['end'].get('dateTime', event['end'].get('date'))
    #     print(start, end, event['summary'])

if __name__ == '__main__':
    main()
