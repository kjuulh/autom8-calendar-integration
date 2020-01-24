import os
import math
import pickle
import datetime
import pendulum

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Calendar():
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.creds = None

        if os.path.exists('token.pkl'):
            with open('token.pkl', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', self.scopes)
                self.creds = flow.run_local_server(port=0)

            with open('token.pkl', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_week(self, date):
        start = date.start_of('week')
        end = date.end_of('week')

        events_result = self.service.events().list(
            calendarId="primary",
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime',
        ).execute()
        return events_result.get('items', [])

    def get_workhours_for_date(self, date):

        events = self.get_week(date)
        hours = 0
        minutes = 0

        for event in events:
            if event['summary'] == 'Work':
                start = event['start'].get(
                    'dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                interval = pendulum.parse(start).diff(pendulum.parse(end))
                hours += interval.hours
                minutes += interval.minutes

        hours += math.floor(minutes/60)
        minutes = minutes % 60

        return hours, minutes
