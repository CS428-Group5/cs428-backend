from .models import BookedSession, MentorSession
from ninja import ModelSchema, Schema, Field
from pydantic import root_validator
from datetime import time, date, datetime, timedelta


class BookedSessionOutSchema(ModelSchema):
    mentee_id: int = Field(alias="mentee.id")
    mentor_id: int = Field(alias="mentor_session.mentor.id")
    session_date: date  = Field(...,alias="mentor_session.session_date")
    session_time: time = Field(...,alias="mentor_session.session_time")
    mentor_first_name: str = Field(...,alias="mentor_session.mentor.user.first_name")
    mentor_last_name: str = Field(...,alias="mentor_session.mentor.user.last_name")
    mentee_first_name: str = Field(...,alias="mentee.user.first_name")
    mentee_last_name: str = Field(...,alias="mentee.user.last_name")

    class Config:
        model = BookedSession
        model_exclude = ["mentee", "mentor_session", "booked_date"]

class MentorSessionInSchema(Schema):
    session_time: time
    session_date: date

class MentorSessionOutSchema(ModelSchema):
    mentor_id: int = Field(..., alias="mentor.id")
    class Config:
        model = MentorSession
        model_exclude = ["mentor"]
