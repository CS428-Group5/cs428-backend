# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.meeting_link, name='meeting_link'),
]
