from django.contrib import admin
from .models import Expertise, Mentor, Mentee, Review


class MentorAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


class MenteeAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


# Register your models here.
admin.site.register(Expertise)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Mentee)
admin.site.register(Review)
