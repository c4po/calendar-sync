from datetime import datetime, timedelta
import win32com.client
from event import Event


class OutlookCalendar:
    def __init__(self):
        self.outlook_mapi = win32com.client.Dispatch(
            'Outlook.Application').GetNamespace('MAPI')
        self.outlook = win32com.client.Dispatch("Outlook.Application")

    def get_outlook_calendar(self, begin, end, prefix):
        calendar = self.outlook_mapi.getDefaultFolder(9).Items
        calendar.IncludeRecurrences = True
        calendar.Sort('[Start]')
        restriction = "[Start] >= '" + begin.strftime(
            '%m/%d/%Y') + "' AND [END] <= '" + end.strftime('%m/%d/%Y') + "'"
        calendar = calendar.Restrict(restriction)
        return list(map(lambda event: Event.outlookEvent(event, prefix), calendar))

    def create_outlook_event(self, event):
        appointment = self.outlook.CreateItem(1)  # 1=outlook appointment item
        appointment.Start = event.start
        appointment.Subject = event.summary
        appointment.body = event.description
        appointment.Duration = int((event.end-event.start).seconds/60)
        appointment.Save()
        return
