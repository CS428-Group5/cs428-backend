from ninja import ModelSchema, Field, Schema
from .models import Mentor, User


class MentorOutSchema(ModelSchema):
    firstname: str = Field(..., max_length=255, alias="user.first_name")
    lastname: str = Field(..., max_length=255, alias="user.last_name")
    title: str = Field(..., max_length=255, alias="user.current_title")

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
