 #run to generate token
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from typing import List, Optional, Type


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events']


def authoriseStuff():
    creds=None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds:
            print("no credentials found")
            return
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_calendar_event(title:str, location:str, startDateTime:str, endDateTime:str, reminderList: Optional[List[str]] = None, recurrenceRules: Optional[List[str]] = None) -> str:
    """Useful to create a calendar event with the provided arguments"""
    event = {
        'summary': title,
        'location': location,
        'start': {
            'dateTime': startDateTime,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': endDateTime,
            'timeZone': 'America/Los_Angeles',
        },
        'reminders': {
            'useDefault': False,
            'overrides':reminderList,
        },
        'recurrence': [
            recurrenceRules
        ],
    }
    print("custom event")
    result= createEvent(event)
    return f"Success: Event created: {result}"

def list_calendar_events(query: Optional[str] = None)-> List[str]:
    """Useful to obtain a list future events alongside their event ids"""
    service= authoriseStuff()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime', q=query).execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return []
    result=[]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        id= event['id']
        result.append(start, event['summary'], id)
        print(start, event['summary'], id)
    return result

def deleteEvent(eventId: str)-> None:
    """Useful to delete an event Calendar given its event id"""
    service= authoriseStuff()
    service.events().delete(calendarId='primary', eventId=eventId).execute()
    return

def createEvent(event):
    service= authoriseStuff()
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
if __name__ == '__main__':
    main()