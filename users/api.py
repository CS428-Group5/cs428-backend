from ninja import Router, Schema, Query
from .models import Mentor, Mentee, Expertise, Review
from core.models import User
from .schemas import *
from typing import List
from enum import Enum
from authentication.helpers import auth_bearer
from session.models import MentorSession

from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q, Value as V
from django.db.models.functions import Concat
from django.http import JsonResponse

from itertools import chain

mentor_router = Router()
user_router = Router()
expertise_router = Router()


class Experience(Enum):
    SHORT = "1-3 years"
    MEDIUM = "3-5 years"
    LONG = ">5 years"


"""
Mentor API
"""


class MentorFilterSchema(Schema):
    limit: int = 100
    offset: int = 0
    price_from: int | None = None
    price_to: int | None = None
    expertise: List[str] | None = None
    experience: List[Experience] | None = None
    name: str | None = None


@mentor_router.get("/", response=List[MentorItemOutSchema])
def get_mentors(
    request,
    filters: MentorFilterSchema = Query(...),
):
    mentors = Mentor.objects.all()
    print(filters.price_from)

    if filters.name is not None:
        mentors = mentors.annotate(
            full_name=Concat("user__first_name", V(" "), "user__last_name")
        ).filter(full_name__icontains=filters.name)

    if filters.expertise is not None:
        mentors = mentors.filter(expertise__expertise_name__in=filters.expertise)

    if filters.experience is not None:
        query = Q()
        if Experience.SHORT in filters.experience:
            query |= Q(experience__lte=3)
        if Experience.MEDIUM in filters.experience:
            query |= Q(experience__range=[3, 5])
        if Experience.LONG in filters.experience:
            query |= Q(experience__gte=5)

        mentors = mentors.filter(query)

    if filters.price_from is not None and filters.price_to is not None:
        mentors = mentors.filter(
            Q(default_session_price__gte=filters.price_from)
            & Q(default_session_price__lte=filters.price_to)
        )

    mentors = mentors.annotate(average_rating=Avg("review__rating"))

    return mentors[filters.offset : filters.offset + filters.limit]


@mentor_router.get("/{int:mentor_id}", response=MentorDetailOutSchema)
def get_mentor_details(request, mentor_id: int):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    return mentor


@mentor_router.get("/{int:mentor_id}/reviews", response=List[ReviewItemSchema])
def get_mentor_reviews(request, mentor_id: int):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    return mentor.review_set.all()


@mentor_router.get("/favorite", auth=auth_bearer, response=List[MentorItemOutSchema])
def get_favorite(request):
    user_id = request.auth
    favorites = get_object_or_404(Mentee, user__id=user_id).favorites.all()
    return favorites


@mentor_router.post("/favorite")
def add_favorite(request, body: FavoriteInSchema):
    mentee_id = 1  # TODO: get from authentication data
    mentor_id = body.mentor_id

    mentee = get_object_or_404(Mentee, id=mentee_id)
    mentor = get_object_or_404(Mentor, id=mentor_id)

    mentee.favorites.add(mentor)

    return JsonResponse({"success": True}, status=200)


@mentor_router.delete("/favorite", auth=auth_bearer)
def delete_favorite(request, body: FavoriteInSchema):
    user_id = request.auth
    mentee = get_object_or_404(Mentee, user__id=user_id)
    mentor = get_object_or_404(Mentor, id=body.mentor_id)

    mentee.favorites.remove(mentor)
    return JsonResponse({}, status=204)


@mentor_router.post("/reviews", auth=auth_bearer)
def add_review(request, body: ReviewInSchema):
    user = get_object_or_404(User, id=request.auth)
    if user.is_mentor:
        return JsonResponse({"msg": "Not authorized"}, status=403)

    mentor = get_object_or_404(Mentor, id=body.mentor_id)
    review = Review(
        mentee=user.mentee, mentor=mentor, content=body.content, rating=body.rating
    )

    review.save()
    return JsonResponse({"success": True}, status=200)


"""
User API
"""


@user_router.get("/my-account-info", auth=auth_bearer)
def get_account_information(request):
    session_user_id = request.auth
    user = get_object_or_404(User, id=session_user_id)
    schema = None

    if user.is_mentor:
        mentor_user = get_object_or_404(Mentor, user__id=session_user_id)
        schema = MentorOutSchema.from_orm(mentor_user)
    else:
        mentee_user = get_object_or_404(Mentee, user__id=session_user_id)
        schema = MenteeOutSchema.from_orm(mentee_user)
    return dict(schema)


@user_router.get("/{id}")
def get_user_information(request, id: int):
    user = get_object_or_404(User, id=id)
    schema = None

    if user.is_mentor:
        mentor_user = get_object_or_404(Mentor, user__id=id)
        schema = MentorOutSchema.from_orm(mentor_user)
    else:
        mentee_user = get_object_or_404(Mentee, user__id=id)
        schema = MenteeOutSchema.from_orm(mentee_user)

    return dict(schema)


@user_router.put("/{id}")
def update_user_information(request, id: int, body: UserUpdateSchema):
    user = get_object_or_404(User, id=id)

    user.first_name = body.first_name
    user.last_name = body.last_name
    user.current_title = body.current_title
    user.about_me = body.about_me
    user.avatar = body.avatar

    if user.is_mentor:
        expertise = get_object_or_404(Expertise, id=body.expertise_id)

        user.mentor.expertise = expertise
        user.mentor.current_company = body.current_company
        user.mentor.default_session_price = body.default_session_price

    user.save()
    return JsonResponse({"success": True}, status=200)

@user_router.get("/purchase-history/", auth=auth_bearer, response=List[PurchaseHistoryOutSchema])
def get_purchase_history(request):
    print(request.auth)
    user = get_object_or_404(User, id=request.auth)
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

"""
Expertises API
"""


@expertise_router.get("/", response=List[ExpertiseSchema])
def get_expertises(request):
    return Expertise.objects.all()
