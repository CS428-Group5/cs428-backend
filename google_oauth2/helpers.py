import requests
from datetime import datetime, timedelta

def create_calendar(
    credentials,
    start_date, 
    start_time, 
    mentor_email, 
    mentee_email
    ):
    headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
    url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1'
    event_props = {
        "end": {
            "date": start_date,
            "time": (datetime.strptime(start_time, "%H:%M:%S") + timedelta(minutes=30)).strftime("%H:%M:%S")
        },
        "start": {
            "date": start_date,
            "time": start_time
        },
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=2"
        ],
        "attendees": [
            {
                "email": mentor_email
            },
            {
                "email": mentee_email
            }
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {
                    "method": "email",
                    "minutes": 60
                },
                {
                    "method": "popup",
                    "minutes": 10
                }
            ]
        },
        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                },
            }
        },
        "summary": "Mentoree's Discussion",
        'location': 'Google Meet',
        'description': "This is the discussion event registered in the Mentoree Website"
    }
    response = requests.post(url, headers=headers, json=event_props).json()
    return response

def cancel_calendar(
    credentials,
    event_id
    ):
    headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
    url = f'https://www.googleapis.com/calendar/v3/calendars/primary/events/{event_id}?sendUpdates=all'
    response = requests.delete(url=url, headers=headers)
    if response.status_code == 204:
        return {"status": "Success"}
    return response.json()
