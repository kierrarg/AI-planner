import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def create_calendar_service(client_secret_file, token_dir, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    creds = None

    # Construct the full path to the token file inside the token_dir
    token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json'
    token_path = os.path.join(token_dir, token_file)

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(f'{API_SERVICE_NAME} {API_VERSION} service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(token_path)
        return None

def create_event(service):
    # Define the event details
    event = {
        'summary': 'Sample Event',
        'description': 'This is a sample event created using Google Calendar API.',
        'start': {
            'dateTime': '2023-08-25T10:00:00',
            'timeZone': 'America/Edmonton',
        },
        'end': {
            'dateTime': '2023-08-25T11:00:00',
            'timeZone': 'America/Edmonton',
        },
    }

    # Insert the event into the primary calendar
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

def delete_custom_event_by_title(title, calendar_service):
    try:
        events = calendar_service.events().list(calendarId='primary').execute()
        for event in events.get('items', []):
            if event['summary'] == title:
                calendar_service.events().delete(calendarId='primary', eventId=event['id']).execute()
                print(f'Event with title "{title}" deleted successfully.')
                return
        print(f'Event with title "{title}" not found.')
    except Exception as e:
        print("An error occurred while deleting events by title:", str(e))

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt