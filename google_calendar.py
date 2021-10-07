from datetime import datetime, timedelta
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from event import Event


class GoogleCalendar:

    def get_calendar_service(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        CREDENTIALS_FILE = "credentials.json"
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('calendar', 'v3', credentials=creds)
        return service

    def __init__(self):
        self.service = self.get_calendar_service()

    def get_google_calendar(self, begin, results, prefix, query=""):
        calendars_result = self.service.events().list(calendarId='primary', timeMin=begin,
                                                      maxResults=results, singleEvents=True, q=query,
                                                      orderBy='startTime').execute()
        events = calendars_result.get('items', [])
        return list(map(lambda event: Event.googleEvent(event, prefix), events))
        # for event in events:

    def create_google_event(self, event):
        event_result = self.service.events().insert(calendarId='primary',
                                                    body={
                                                        "summary": event.summary,
                                                        "description": event.description,
                                                        "start": {"dateTime": event.start.isoformat(), "timeZone": 'America/Toronto'},
                                                        "end": {"dateTime": event.end.isoformat(), "timeZone": 'America/Toronto'},
                                                    }
                                                    ).execute()
        return event_result

    def delete_google_event(self, event):
        event_result = self.service.events().delete(calendarId='primary',
                                                    eventId=event.eventid
                                                    ).execute()
        return event_result
