 #run to generate token
from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz
from typing import List, Optional, Type
from datetime import timedelta, datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events']


def authoriseStuff():
    creds=None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds:
            print("no credentials found")
            raise Exception("no credentials found")
    service = build('calendar', 'v3', credentials=creds)
    return service

def currentDateTime()->str:
    """This function helps to get the current date time
    :return: current date time
    """
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    return now

def create_calendar_event(title:str, location:str, startDateTime:str, endDateTime:str, reminderList: Optional[List[str]] = None, recurrenceRules: Optional[List[str]] = None) -> str:
    """This function helps to create a calendar event given its details
    :param title: title of the event
    :param location: location of the event
    :param startDateTime: start date time of the event
    :param endDateTime: end date time of the event
    :param reminderList: list of reminders
    :param recurrenceRules: list of recurrence rules, must include end date in basic ISO 8601 date format
    :return: html link to the event
    """
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
    result= createEvent(event)
    return f"Success: Event created: {result}"

def list_calendar_events_today()->List[str]:
    pacific = pytz.timezone('America/Los_Angeles')
    now = datetime.now(pacific)
    timeMin = now.replace(hour=0, minute=0, second=0, microsecond=0)
    timeMin_str = timeMin.isoformat()
    timeMax = timeMin + timedelta(days=1)
    timeMax_str = timeMax.isoformat()
    service= authoriseStuff()
    events_result = service.events().list(calendarId='primary', timeMin=timeMin_str,
                                              singleEvents=True, timeMax=timeMax_str,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
        return []
    result=[]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        id= event['id']
        result.append([start, event['summary'], id])
    return result

def list_calendar_events(calendarEventTitle: Optional[str] = None)-> List[str]:
    """This function helps to list calendar events given its optional title
    :param calendarEventTitle: title of the event (optional)
    :return: list of events
    """
    service= authoriseStuff()
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime', q=calendarEventTitle).execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return []
    result=[]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        id= event['id']
        result.append([start, event['summary'], id])
    return result

def get_start_end_rfc3339(dateTime):
    #dateTime_obj = datetime.fromisoformat(dateTime)
    dateTime_obj = datetime.fromisoformat(dateTime).astimezone(pytz.timezone('America/Los_Angeles'))
    start_of_day = dateTime_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1) - timedelta(microseconds=1)
    start_rfc3339 = start_of_day.isoformat()
    end_rfc3339 = end_of_day.isoformat()
    return start_rfc3339, end_rfc3339

def list_calendar_events_simple(dateTime)-> List[str]:
    """This function helps to list calendar events on a particular day
    :param dateTime: date to list events
    :return: list of events
    """
    start,end= get_start_end_rfc3339(dateTime)
    service= authoriseStuff()
    events_result = service.events().list(calendarId='primary', timeMin=start,timeMax=end,
                                              maxResults=10, singleEvents=False).execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
        return []
    result=[]
    for event in events:
        summary= event['summary']
        if "medication" in summary: #skip medication events from getting deleted
            continue
        start = event['start'].get('dateTime', event['start'].get('date'))
        id= event['id']
        result.append([start, summary, id])
    return result

def deleteEvent(eventId: str)-> None:
    """This function helps to delete a calendar event given its id
    :param eventId: id of the event
    :return: None
    """
    service= authoriseStuff()
    service.events().delete(calendarId='primary', eventId=eventId).execute()
    return

def deleteEventsDate(date: str)-> None:
    """This function helps to delete calendar events on a particular date
    :param date: date to clear events
    :return: None
    """
    service= authoriseStuff()
    events= list_calendar_events_simple(date)
    for e in events:
        service.events().delete(calendarId='primary', eventId=e[2]).execute()
    return

def createEvent(event):
    print("called createEvent")
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
    #create_calendar_event(title="Take Diabetes Medications", location="Home", startDateTime="2023-11-19T13:00:00", endDateTime="2023-11-19T13:15:00", recurrenceRules=["RRULE:FREQ=DAILY;COUNT=30"], reminderList=["15 minutes"])
    #print(list_calendar_events_simple("2023-11-23"))
    #deleteEventsDate("2023-11-24")