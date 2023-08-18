from ninja import Router
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction
from django.contrib.sessions.models import Session
from base.settings import cur_deployed_host, MEETING_RETURN_URL_HOST

from session.models import MentorSession, BookedSession
from authentication.helpers import auth_bearer
from users.models import Mentor, Mentee, User
from .schemas import (
    MentorSessionInSchema,
    MentorSessionOutSchema,
    BookedSessionOutSchema,
)
from google_oauth2.helpers import create_calendar, cancel_calendar

from typing import List
from itertools import chain
from datetime import datetime, timedelta

session_router = Router()


@session_router.get(
    "/mentor_sessions/{mentor_session_id}", response=MentorSessionOutSchema
)
def get_single_mentor_session(request, mentor_session_id: int):
    return get_object_or_404(MentorSession, id=mentor_session_id)


@session_router.post("/mentor_sessions", auth=auth_bearer)
def add_mentor_session(request, body: MentorSessionInSchema):
    mentor = get_object_or_404(Mentor, user_id=request.auth)
    if MentorSession.objects.filter(
        mentor_id=mentor.id,
        session_time=body.session_time,
        session_date=body.session_date,
    ):
        raise ValueError("The datetime has been allocated")
    MentorSession.objects.create(
        mentor_id=mentor.id,
        session_time=body.session_time,
        session_date=body.session_date,
        session_price=mentor.default_session_price,
        is_book=False,
    )
    return JsonResponse({"success": True}, status=200)


@session_router.get(
    "/{mentor_id}/mentor_sessions/all", response=List[MentorSessionOutSchema]
)
def get_mentor_session(request, mentor_id: int):
    mentor_sessions = filter(
        lambda mentor_session: not mentor_session.is_book,
        MentorSession.objects.filter(mentor_id=mentor_id),
    )
    return list(mentor_sessions)


@session_router.delete("/mentor_sessions/{mentor_session_id}", auth=auth_bearer)
def delete_mentor_session(request, mentor_session_id: int):
    mentor = get_object_or_404(Mentor, user_id=request.auth)
    mentor_session = get_object_or_404(
        MentorSession, id=mentor_session_id, mentor=mentor.id
    )
    if BookedSession.objects.filter(mentor_session=mentor_session):
        return JsonResponse(
            {"error": "Cancel the relevant booked session first"}, status=403
        )
    mentor_session.delete()
    return JsonResponse({"success": True}, status=200)


@session_router.post("/booked_session/{mentor_session_id}", auth=auth_bearer)
@transaction.atomic
def add_booked_session(request, mentor_session_id: int):
    mentor_session = get_object_or_404(MentorSession, id=mentor_session_id)
    mentee = get_object_or_404(Mentee, user_id=request.auth)

    mentor_session.is_book = True
    mentor_session.save()
    BookedSession.objects.create(
        mentee_id=mentee.id,
        mentor_session_id=mentor_session.id,
        booked_date=datetime.now().strftime("%Y-%m-%d"),
        cancelled_by=0,
    )
    return JsonResponse({"success": True}, status=200)


@session_router.get(
    "/booked_session/{user_id}/all", response=List[BookedSessionOutSchema]
)
def get_all_booked_sessions(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    if user.is_mentor:
        mentor = get_object_or_404(Mentor, user=user)
        mentor_sessions = MentorSession.objects.filter(mentor=mentor)
        book_sessions = chain(
            *map(
                lambda mentor_session: BookedSession.objects.filter(
                    mentor_session=mentor_session
                ),
                mentor_sessions,
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

    mentor_session = get_object_or_404(
        MentorSession, id=booked_session.mentor_session_id
    )
    mentor_session.is_book = False
    mentor_session.save()
    return JsonResponse({"success": True}, status=200)


@session_router.get(
    "/booked_session/{booked_session_id}/meeting_link", auth=auth_bearer
)
def get_booked_session_meeting(request, booked_session_id: int):
    user = get_object_or_404(User, id=request.auth)
    booked_session = get_object_or_404(BookedSession, id=booked_session_id)
    if user.is_mentor:
        if booked_session.mentor_session.mentor.user.id != user.id:
            raise KeyError("User and BookedSession don't match with each other")
    else:
        if booked_session.mentee.user.id != user.id:
            raise KeyError("User and BookedSession don't match with each other")

    meeting_url = (
        f"http://{cur_deployed_host}:8000/meeting?"
        f"session_id={booked_session.id}&"
        f"""full_name={user.first_name + " " + user.last_name}&"""
        f"user_id={user.id}&"
        f"redirect_url={MEETING_RETURN_URL_HOST}"
    )
    return JsonResponse({"meeting_url": meeting_url}, status=200)
