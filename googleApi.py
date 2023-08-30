import datetime
import google.oauth2.credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_event():
    # Load credentials from file
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    try: 
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file(r'C:\Users\kikig\Documents\programs\Python\PlannerApp\AI-planner\credentials.JSON', scopes=SCOPES)
    
        # Building API services
        service = build('calendar', 'v3', credentials=creds)

        # Define the event
        event = {
            'summary': 'Sample',
            'description': 'Sample event using Google API',
            'start': {
                'dateTime': '2023-08-25T10:00:00',
                'timeZone': 'America/Edmonton',
            },
            'end': {
                'dateTime': '2023-08-25T11:00:00',
                'timeZone': 'America/Edmonton',
            },
        }

        # Create the event
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_event()