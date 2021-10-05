from datetime import datetime, timedelta
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

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

    def get_google_calendar(self, begin, results, query=""):
        calendars_result = self.service.events().list(calendarId='primary', timeMin=begin,
                                        maxResults=results, singleEvents=True, q=query,
                                        orderBy='startTime').execute()
        events = calendars_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            print(start, end, event['summary'])

    def create_google_event(self, start, duration, subject, description):
        end = start + timedelta(minutes=duration)
        event_result = self.service.events().insert(calendarId='primary',
           body={
               "summary": subject,
               "description": description,
               "start": {"dateTime": start.isoformat(), "timeZone": 'America/Toronto'},
               "end": {"dateTime": end.isoformat(), "timeZone": 'America/Toronto'},
           }
        ).execute()
