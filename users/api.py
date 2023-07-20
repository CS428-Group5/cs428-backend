from ninja import Router, Schema, Query
from .models import Mentor, Mentee, Expertise
from core.models import User
from .schemas import (
    MentorItemOutSchema,
    MentorDetailOutSchema,
    FavoriteInSchema,
    MentorOutSchema,
    MenteeOutSchema,
    ReviewItemSchema,
    ExpertiseSchema,
)
from typing import List, Optional
from enum import Enum

from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q
from django.http import JsonResponse

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


@mentor_router.get("/", response=List[MentorItemOutSchema])
def get_mentors(
    request,
    filters: MentorFilterSchema = Query(...),
):
    mentors = Mentor.objects.all()
    print(filters.price_from)

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


@mentor_router.post("/favorite")
def add_favorite(request, body: FavoriteInSchema):
    mentee_id = 1  # TODO: get from authentication data
    mentor_id = body.mentor_id

    mentee = get_object_or_404(Mentee, id=mentee_id)
    mentor = get_object_or_404(Mentor, id=mentor_id)

    mentee.favorites.add(mentor)

    return JsonResponse({"success": True}, status=200)


"""
User API
"""


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


"""
Expertises API
"""


@expertise_router.get("/", response=List[ExpertiseSchema])
def get_expertises(request):
    return Expertise.objects.all()
