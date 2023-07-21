from ninja import Router, Form, Schema

from users.models import User, Expertise
from .helpers import create_token, auth_bearer

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, JsonResponse

authenticate_router = Router()


class MenteeInSchema(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    gender: int
    current_title: str
    about_me: str = None


class MentorInSchema(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    gender: int
    current_title: str
    about_me: str = None
    current_company: str = None
    default_session_price: float = 50
    experience: int = 0
    expertise_name: str = None


@authenticate_router.post("/registration/mentor")
def registration_mentor(request, mentor_schema: MentorInSchema):
    hashed_password = make_password(mentor_schema.password)
    user = User.objects.create(username=mentor_schema.username,
                               password=hashed_password,
                               email=mentor_schema.email,
                               first_name=mentor_schema.first_name,
                               last_name=mentor_schema.last_name,
                               gender=mentor_schema.gender,
                               current_title=mentor_schema.current_title,
                               about_me=mentor_schema.about_me,
                               is_mentor=True,
                               is_staff=False)
    expertise = Expertise.objects.get(expertise_name=mentor_schema.expertise_name)
    user.mentor.expertise = expertise
    user.mentor.current_company = mentor_schema.current_company
    user.mentor.default_session_price = mentor_schema.default_session_price
    user.mentor.experience = mentor_schema.experience
    user.save()
    return {"mentor_id": user.id}


@authenticate_router.post("/registration/mentee")
def registration_mentee(request, mentee_schema: MenteeInSchema):
    hashed_password = make_password(mentee_schema.password)
    mentee_user = User.objects.create(username=mentee_schema.username,
                                      password=hashed_password,
                                      email=mentee_schema.email,
                                      first_name=mentee_schema.first_name,
                                      last_name=mentee_schema.last_name,
                                      gender=mentee_schema.gender,
                                      current_title=mentee_schema.current_title,
                                      about_me=mentee_schema.about_me,
                                      is_mentor=False,
                                      is_staff=False)
    return {"mentee_id": mentee_user.id}


@authenticate_router.post("/login")
def login(request, username: str = Form(...), password: str = Form(...)):
    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            token = create_token(user.id, username)
            return JsonResponse({"token": token}, status=200)
        else:
            return HttpResponse(content="Invalid Username or Password", status=401)
    except ObjectDoesNotExist:
        return HttpResponse(content="Invalid Username or Password", status=401)

@authenticate_router.get("/logout")
def logout(request):
    return HttpResponse("Successfully Logout", status=200)

@authenticate_router.post("/password_change", auth=auth_bearer)
def password_change(
    request,
    username: str = Form(...),
    old_password: str = Form(...),
    new_password: str = Form(...),
):
    session_user_id = request.auth
    session_user = User.objects.get(id=session_user_id)
    if session_user.username == username and check_password(old_password, session_user.password):
        session_user.password = make_password(new_password)
        session_user.save()
        return HttpResponse("Successfully Change Password", status=200)
    else:
        return HttpResponse("Invalid Username or Password", status=400)
