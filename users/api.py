from ninja import Router
from .models import Mentor
from .schemas import MentorOutSchema, MentorDetailOutSchema
from typing import List

from django.shortcuts import get_object_or_404

mentor_router = Router()
user_router = Router()


@mentor_router.get("/", response=List[MentorOutSchema])
def get_mentors(request):
    mentors = Mentor.objects.all()
    return mentors


@mentor_router.get("/{mentor_id}", response=MentorDetailOutSchema)
def get_mentor_details(request, mentor_id: int):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    return mentor
