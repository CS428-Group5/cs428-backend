from ninja import Router
import requests
from django.http import HttpResponseRedirect, JsonResponse
import json

google_oauth2_router = Router()

CLIENT_ID = '1063195259566-3lf5ooc0g9ltouvdle1op5geu058r9je.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SCOPE = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events'
REDIRECT_URI = 'http://localhost:8000/api/google-oauth2/oauth2callback'

@google_oauth2_router.get("/index")
def index(request):
    print("baka:", request.GET)
    if 'credentials' not in request.session:
        return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
    credentials = json.loads(request.session['credentials'])
    if credentials['expires_in'] <= 0:
        return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
    else:
        headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
        url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1'
        event_props = {
            "end": {
                "date": "2023-08-01"
            },
            "start": {
                "date": "2023-07-31"
            },
            "recurrence": [
                "RRULE:FREQ=DAILY;COUNT=2"
            ],
            "attendees": [
                {
                    "email": "quocnguyendinh121@gmail.com"
                },
                {
                    "email": "ndquoc20@apcs.fitus.edu.vn"
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
            "summary": "Mentoree",
            'location': 'Mentoree Website',
            'description': "A chance to hear more about Google's developer products."
        }
        response = requests.post(url, headers=headers, json=event_props).json()
        try:
            return JsonResponse({"Event created": response["htmlLink"]}, status=200)
        except KeyError:
            del request.session['credentials']
            return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
        
@google_oauth2_router.get("/oauth2callback")
def oauth2callback(request):
    print(request.GET)
    if 'code' not in request.GET:
        auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                    '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
        return JsonResponse({"Google Oauth2 Link": auth_uri}, status=200)
    else:
        auth_code = request.GET.get('code')
        data = {'code': auth_code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'}
        r = requests.post('https://oauth2.googleapis.com/token', data=data)
        request.session['credentials'] = r.text
        return HttpResponseRedirect("/api/google-oauth2/index")

@google_oauth2_router.get("/oauth2clear")
def oauth2clear(request):
    if 'credentials' in request.session:
        del request.session['credentials']
        return "Succesfully delete the credential out of the request session"
