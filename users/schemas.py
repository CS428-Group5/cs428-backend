from ninja import ModelSchema, Field, Schema
from .models import Mentor, User


class MentorOutSchema(Schema):
    firstname: str = Field(..., max_length=255, alias="user.firstname")
    lastname: str = Field(..., max_length=255, alias="user.lastname")
    experience: int
    default_session_price: float
