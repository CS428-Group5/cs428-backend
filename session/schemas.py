from .models import BookedSession, MentorSession
from ninja import ModelSchema, Schema, Field
from datetime import time, date


class BookedSessionOutSchema(ModelSchema):
    mentee_id: int = Field(alias="mentee.id")
    class Config:
        model = BookedSession
        model_exclude = ["mentee"]

class MentorSessionInSchema(Schema):
    session_time: time
    session_date: date

class MentorSessionOutSchema(ModelSchema):
    mentor_id: int = Field(..., alias="mentor.id")
    class Config:
        model = MentorSession
        model_exclude = ["mentor"]
