from .models import BookedSession, MentorSession
from ninja import ModelSchema, Schema
from datetime import time, date


class BookedSessionOutSchema(ModelSchema):
    class Config:
        model = BookedSession
        model_fields = "__all__"

class MentorSessionInSchema(Schema):
    session_time: time
    session_date: date
    is_book: bool = False

class MentorSessionOutSchema(ModelSchema):
    class Config:
        model = MentorSession
        model_fields = "__all__"
