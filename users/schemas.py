from ninja import ModelSchema, Field, Schema
from .models import Mentor, Mentee, Review, Expertise
from core.models import User
from session.models import BookedSession

from datetime import date, time

"""
Mentor schemas
"""


class MentorItemOutSchema(ModelSchema):
    firstname: str = Field(..., max_length=255, alias="user.first_name")
    lastname: str = Field(..., max_length=255, alias="user.last_name")
    current_title: str = Field(..., max_length=255, alias="user.current_title")
    avatar: str | None = Field(..., max_length=255, alias="user.avatar")
    average_rating: float | None = None

    class Config:
        model = Mentor
        model_fields = ["id", "experience", "current_company", "default_session_price"]


class MentorDetailOutSchema(ModelSchema):
    firstname: str = Field(..., max_length=255, alias="user.first_name")
    lastname: str = Field(..., max_length=255, alias="user.last_name")
    about_me: str = Field(..., max_length=255, alias="user.about_me")
    expertise: str = Field(..., max_length=255, alias="expertise.expertise_name")
    current_title: str = Field(..., max_length=255, alias="user.current_title")

    class Config:
        model = Mentor
        model_fields = [
            "id",
            "experience",
            "current_company",
            "default_session_price",
        ]


class FavoriteInSchema(Schema):
    mentor_id: int


class ReviewInSchema(Schema):
    mentor_id: int
    rating: int = Field(..., ge=1, le=5)
    content: str


class ReviewItemSchema(ModelSchema):
    firstname: str = Field(..., max_length=255, alias="mentee.user.first_name")
    lastname: str = Field(..., max_length=255, alias="mentee.user.last_name")
    avatar: str | None = Field(..., max_length=255, alias="mentee.user.avatar")

    class Config:
        model = Review
        model_fields = ["id", "content", "rating"]


"""
User schemas
"""


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "avatar",
            "about_me",
            "current_title",
            "email",
            "is_mentor",
        ]


class MenteeOutSchema(ModelSchema):
    user: UserSchema

    class Config:
        model = Mentee
        model_exclude = ["favorites"]


class MentorOutSchema(ModelSchema):
    user: UserSchema

    class Config:
        model = Mentor
        model_fields = [
            "id",
            "expertise",
            "current_company",
            "default_session_price",
        ]


class UserUpdateSchema(Schema):
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    about_me: str = Field(..., max_length=255)
    current_title: str = Field(..., max_length=255)
    avatar: str | None = Field(..., max_length=255)

    # Additional fields for mentor
    expertise_id: int | None
    current_company: str | None
    default_session_price: float | None

class PurchaseHistoryOutSchema(ModelSchema):
    mentee_id: int = Field(alias="mentee.id")
    mentee_user_id: int = Field(..., alias="mentee.user.id")
    mentor_id: int = Field(alias="mentor_session.mentor.id")
    mentor_user_id: int = Field(..., alias="mentor_session.mentor.user.id")
    session_date: date  = Field(...,alias="mentor_session.session_date")
    session_time: time = Field(...,alias="mentor_session.session_time")
    session_price: float | None = Field(...,alias="mentor_session.session_price")
    mentor_first_name: str = Field(...,alias="mentor_session.mentor.user.first_name")
    mentor_last_name: str = Field(...,alias="mentor_session.mentor.user.last_name")
    mentee_first_name: str = Field(...,alias="mentee.user.first_name")
    mentee_last_name: str = Field(...,alias="mentee.user.last_name")

    class Config:
        model = BookedSession
        model_exclude = ["mentee", "mentor_session"]

"""
Other Schemas
"""


class ExpertiseSchema(ModelSchema):
    class Config:
        model = Expertise
        model_fields = "__all__"
