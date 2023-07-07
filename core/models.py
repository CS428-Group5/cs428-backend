from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Gender(models.IntegerChoices):
        FEMALE = 0, "Female"
        MALE = 1, "Male"

    id = models.BigAutoField(primary_key=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    gender = models.IntegerField(choices=Gender.choices, null=True, blank=True)
    current_title = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    is_mentor = models.BooleanField(default=False)
