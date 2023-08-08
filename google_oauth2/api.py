from ninja import Router
import requests
from django.http import HttpResponseRedirect, JsonResponse
import json
from datetime import datetime, timedelta

google_oauth2_router = Router()

CLIENT_ID = '1063195259566-3lf5ooc0g9ltouvdle1op5geu058r9je.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SCOPE = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events'
REDIRECT_URI = 'http://localhost:8000/api/google-oauth2/oauth2callback'
        
@google_oauth2_router.get("/oauth2callback")
def oauth2callback(request):
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
        session_id = request.session.session_key
        return HttpResponseRedirect(f"http://localhost:5173?session_id={session_id}")

@google_oauth2_router.get("/oauth2clear")
def oauth2clear(request):
    if 'credentials' in request.session:
        del request.session['credentials']
        return "Succesfully delete the credential out of the request session"
