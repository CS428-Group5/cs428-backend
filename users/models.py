from typing import Iterable, Optional
from django.db import models
from core.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

class Expertise(models.Model):
    expertise_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.expertise_name


##################################################################################


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_company = models.CharField(max_length=255, null=True, blank=True)
    default_session_price = models.DecimalField(
        max_digits=13, decimal_places=4, null=True, blank=True
    )
    experience = models.IntegerField(null=True, blank=True)
    expertise = models.ForeignKey(Expertise, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Mentor, related_name="favorites", blank=True)

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def create_new_user(sender, instance, created, **kwargs):
    if created:
        if instance.is_mentor:
            Mentor.objects.create(user=instance)
        else:
            Mentee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    if instance.is_mentor:
        instance.mentor.save()
    else:
        instance.mentee.save()


##################################################################################


class Review(models.Model):
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    rating = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

##################################################################################
