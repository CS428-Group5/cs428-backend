from django.contrib import admin
from .models import BookedSession, MentorSession

# Register your models here.
admin.site.register(BookedSession)
admin.site.register(MentorSession)