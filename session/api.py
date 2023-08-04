from ninja import Router
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction

from session.models import MentorSession, BookedSession
from authentication.helpers import auth_bearer
from users.models import Mentor, Mentee, User
from .schemas import MentorSessionInSchema, MentorSessionOutSchema, BookedSessionOutSchema
from google_oauth2.helpers import create_calendar, cancel_calendar

from typing import List
from itertools import chain
import json
from datetime import datetime, timedelta

session_router= Router()

@session_router.post("/mentor_sessions", auth=auth_bearer)
def add_mentor_session(request, body: MentorSessionInSchema):
    mentor = get_object_or_404(Mentor, user_id=request.auth)
    if MentorSession.objects.filter(mentor_id=mentor.id, session_time=body.session_time, session_date=body.session_date):
        raise ValueError("The datetime has been allocated")
    MentorSession.objects.create(
        mentor_id=mentor.id,
        session_time=body.session_time,
        session_date=body.session_date,
        is_book=False
    )
    return JsonResponse({"success": True}, status=200)

@session_router.get("/{mentor_id}/mentor_sessions/all", response=List[MentorSessionOutSchema])
def get_mentor_session(request, mentor_id: int):
    return MentorSession.objects.filter(mentor_id=mentor_id)

@session_router.delete("/mentor_sessions/{mentor_session_id}" , auth=auth_bearer)
def delete_mentor_session(request, mentor_session_id: int):
    mentor = get_object_or_404(Mentor, user_id=request.auth)
    mentor_session = get_object_or_404(MentorSession, id=mentor_session_id, mentor=mentor.id)
    if BookedSession.objects.filter(mentor_session=mentor_session):
        return JsonResponse({"error": "Cancel the relevant booked session first"}, status=403)
    mentor_session.delete()
    return JsonResponse({"success": True}, status=200)


@session_router.post("/booked_session/{mentor_session_id}", auth=auth_bearer)
@transaction.atomic
def add_booked_session(request, mentor_session_id: int):
    mentor_session = get_object_or_404(MentorSession, id=mentor_session_id)
    mentee = get_object_or_404(Mentee, user_id=request.auth)
    mentor = get_object_or_404(Mentor, id=mentor_session.mentor.id)
    
    if 'credentials' not in request.session:
        return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
    
    credentials = json.loads(request.session['credentials'])
    if credentials['expires_in'] <= 0:
        return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
    else:
        if mentor_session.is_book:
            return JsonResponse({"error": "The session has been already booked"}, status=403)
        
        start_date_time = datetime.strptime(
            str(mentor_session.session_date) + " " + str(mentor_session.session_time),
            '%Y-%m-%d %H:%M:%S'
        )
        end_date_time = start_date_time + timedelta(minutes=30)
        response = create_calendar(
                credentials=credentials,
                start_date_time=start_date_time.strftime('%Y-%m-%dT%H:%M:%S.000+07:00'),
                end_date_time=end_date_time.strftime('%Y-%m-%dT%H:%M:%S.000+07:00'),
                mentee_email=mentee.user.email,
                mentor_email=mentor.user.email
            )
        if "error" in response:
            if response["error"]["status"] == "UNAUTHENTICATED":
                del request.session['credentials']
                return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
            
        mentor_session.is_book = True
        mentor_session.save()
        BookedSession.objects.create(
                mentee_id=mentee.id,
                mentor_session_id=mentor_session.id,
                event_id=response["id"],
                event_link=response["htmlLink"],
                cancelled_by=0
            )
        return JsonResponse({"success": True}, status=200)

@session_router.get("/booked_session/{user_id}/all", response=List[BookedSessionOutSchema])
def get_all_booked_sessions(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    if user.is_mentor:
        mentor = get_object_or_404(Mentor, user=user)
        mentor_sessions = MentorSession.objects.filter(mentor=mentor)
        book_sessions = chain(
            *map(
                lambda mentor_session: BookedSession.objects.filter(mentor_session=mentor_session),
                mentor_sessions
            )
        )
        return list(book_sessions)
    else:
        mentee = get_object_or_404(Mentee, user=user)
        return BookedSession.objects.filter(mentee=mentee)


@session_router.post("/booked_session/{booked_session_id}/canceled", auth=auth_bearer)
@transaction.atomic
def cancel_booked_session(request, booked_session_id: int):
    user = get_object_or_404(User, id=request.auth)

    booked_session = get_object_or_404(BookedSession, id=booked_session_id)
    booked_session.cancelled_by = 1 if user.is_mentor else 2
    booked_session.save()

    mentor_session = get_object_or_404(MentorSession, id=booked_session.mentor_session_id)
    mentor_session.is_book = False
    mentor_session.save()

    if 'credentials' not in request.session:
        return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
    
    credentials = json.loads(request.session['credentials'])
    if credentials['expires_in'] <= 0:
        return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
    else:
        response = cancel_calendar(credentials, booked_session.event_id)
        if "error" in response:
            if "status" in response["error"]:
                if response["error"]["status"] == "UNAUTHENTICATED":
                    del request.session['credentials']
                    return HttpResponseRedirect("/api/google-oauth2/oauth2callback")
            raise ValueError(response)
        return JsonResponse({"success": True}, status=200)