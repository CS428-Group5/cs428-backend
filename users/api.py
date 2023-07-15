from ninja import Router
from .models import Mentor, Mentee
from core.models import User
from .schemas import (
    MentorItemOutSchema,
    MentorDetailOutSchema,
    FavoriteInSchema,
    MentorOutSchema,
    MenteeOutSchema,
)
from typing import List

from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q

mentor_router = Router()
user_router = Router()

"""
Mentor API
"""


@mentor_router.get("/", response=List[MentorItemOutSchema])
def get_mentors(
    request,
    offset: int = 0,
    limit: int = 6,
    expertise: str = None,
    price_from: int = None,
    price_to: int = None,
):
    mentors = Mentor.objects.all()

    if expertise is not None:
        mentors = mentors.filter(expertise__expertise_name__icontains=expertise)

    if price_from is not None and price_to is not None:
        mentors = mentors.filter(
            Q(default_session_price__gte=price_from)
            & Q(default_session_price__lte=price_to)
        )

    mentors = Mentor.objects.annotate(average_rating=Avg("review__rating"))

    return mentors[offset : offset + limit]


@mentor_router.get("/{mentor_id}", response=MentorDetailOutSchema)
def get_mentor_details(request, mentor_id: int):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    return mentor


@mentor_router.post("/favorite")
def add_favorite(request, body: FavoriteInSchema):
    user_id = 1  # TODO: get from authentication data
    mentor_id = body.mentor_id

    mentee = get_object_or_404(Mentee, user__id=user_id)
    mentor = get_object_or_404(Mentor, id=mentor_id)

    mentee.favorites.add(mentor)

    return {"success": True}


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
