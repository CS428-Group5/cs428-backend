from ninja import ModelSchema, Field, Schema
from .models import Mentor, Mentee
from core.models import User

"""
Mentor schemas
"""


class MentorItemOutSchema(ModelSchema):
    firstname: str = Field(..., max_length=255, alias="user.first_name")
    lastname: str = Field(..., max_length=255, alias="user.last_name")
    title: str = Field(..., max_length=255, alias="user.current_title")
    average_rating: float | None = None

    class Config:
        model = Mentor
        model_fields = ["id", "experience", "current_company", "default_session_price"]


class MentorDetailOutSchema(ModelSchema):
    firstname: str = Field(..., max_length=255, alias="user.first_name")
    lastname: str = Field(..., max_length=255, alias="user.last_name")
    title: str = Field(..., max_length=255, alias="user.current_title")
    about_me: str = Field(..., max_length=255, alias="user.about_me")
    expertise: str = Field(..., max_length=255, alias="expertise.expertise_name")

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
            "is_mentor",
        ]


class MenteeOutSchema(ModelSchema):
    user: UserSchema

    class Config:
        model = Mentee
        model_exclude = ["favorites", "id"]


class MentorOutSchema(ModelSchema):
    user: UserSchema

    class Config:
        model = Mentor
        model_fields = [
            "expertise",
            "current_company",
            "default_session_price",
        ]
