from ninja import Router, Form, Schema

from users.models import Mentee, Mentor, User, Expertise

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse

from helpers import verify_token, create_token

authenticate_router = Router()

class UserInSchema(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    gender: int
    current_title: str
    about_me: str = None

class MentorInSchema(Schema):
    current_company: str= None
    default_session_price: float = 50
    experience: int = 0
    expertise_name: str= None

@authenticate_router.post("/registration/mentor")
def registration_mentor(request, user_schema: UserInSchema, mentor_schema: MentorInSchema):
    user = User.objects.create(**(user_schema.dict()), is_mentor=True, is_staff=False)
    expertise=Expertise.objects.get(expertise_name=mentor_schema.expertise_name)
    mentor = Mentor.objects.create(
        user=user,
        expertise=expertise,
        current_company=mentor_schema.current_company,
        default_session_price=mentor_schema.default_session_price,
        experience=mentor_schema.experience
    )
    return {"mentor_id": mentor.id}

@authenticate_router.post("/registration/mentee")
def registration_mentee(request, user_schema: UserInSchema):
    user = User.objects.create(**(user_schema.dict()), is_mentor=False, is_staff=False)
    mentee = Mentee.objects.create(user=user)
    return {"mentee_id": mentee.id}

@authenticate_router.post("/login")
def login(request, username: str = Form(...), password: str = Form(...)):
    try:
        user_id = User.objects.get(username=username,  password=password)
        token = create_token(user_id, username)
        return HttpResponse(token, status=200)
    except ObjectDoesNotExist:
        return HttpResponse(content="Invalid Username or Password", status=403)

@authenticate_router.get("/logout")
def logout(request):
    pass

@authenticate_router.post("/password_change")
def password_change(request, user: str = Form(...), old_password: str = Form(...), new_password: str = Form(...)):
    pass


