from typing import Any, Optional
from ninja import Router, Form, Schema

from users.models import User, Expertise
from .helpers import create_token, cookie_key

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse


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
    current_company: str= None
    default_session_price: float = 50
    experience: int = 0
    expertise_name: str= None

@authenticate_router.post("/registration/mentor")
def registration_mentor(request, mentor_schema: MentorInSchema):
    user = User.objects.create(username=mentor_schema.username,
                               password=mentor_schema.password,
                               email=mentor_schema.email,
                               first_name=mentor_schema.first_name,
                               last_name=mentor_schema.last_name,
                               gender=mentor_schema.gender,
                               current_title=mentor_schema.current_title,
                               about_me=mentor_schema.about_me,
                               is_mentor=True, 
                               is_staff=False)
    expertise=Expertise.objects.get(expertise_name=mentor_schema.expertise_name)
    user.mentor.expertise=expertise
    user.mentor.current_company=mentor_schema.current_company
    user.mentor.default_session_price=mentor_schema.default_session_price
    user.mentor.experience=mentor_schema.experience
    user.save()
    return {"mentor_id": user.id}

@authenticate_router.post("/registration/mentee")
def registration_mentee(request, mentee_schema: MenteeInSchema):
    mentee_user = User.objects.create(username=mentee_schema.username,
                               password=mentee_schema.password,
                               email=mentee_schema.email,
                               first_name=mentee_schema.first_name,
                               last_name=mentee_schema.last_name,
                               gender=mentee_schema.gender,
                               current_title=mentee_schema.current_title,
                               about_me=mentee_schema.about_me,
                               is_mentor=True, 
                               is_staff=False)
    return {"mentee_id": mentee_user.id}

@authenticate_router.post("/login")
def login(request, username: str = Form(...), password: str = Form(...)):
    try:
        user = User.objects.get(username=username,  password=password)
        token = create_token(user.id, username)
        request.session['token'] = token
        return HttpResponse("Succesfully login", status=200)
    except ObjectDoesNotExist:
        return HttpResponse(content="Invalid Username or Password", status=403)
    
@authenticate_router.get("/cookie-acceptance")
def cookie_acceptance(request):
    if request.session.test_cookie_worked():
        return HttpResponse("Client Accept Cookie", status=200)
    else:
        request.session.set_test_cookie()
        return HttpResponse("Client Not Accept Cookie", status=302)

@authenticate_router.get("/logout")
def logout(request):
    if 'token' in request.session:
        del request.session['token']
    return HttpResponse("Successfully Logout", status=200)

@authenticate_router.post("/password_change", auth=cookie_key)
def password_change(request, username: str = Form(...), old_password: str = Form(...), new_password: str = Form(...)):
    session_user_id = request.auth
    session_user = User.objects.get(id=session_user_id)
    if session_user.username == username and session_user.password == old_password:
        session_user.password = new_password
        session_user.save()
        return HttpResponse("Successfully Change Password", status=200)
    else:
        return HttpResponse("Invalid Username or Password", status=400)


