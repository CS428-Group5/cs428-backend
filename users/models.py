from django.db import models
from core.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Expertise(models.Model):
    expertise_name = models.CharField(max_length=255)


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_company = models.CharField(max_length=255, null=True, blank=True)
    default_session_price = models.DecimalField()
    experience = models.IntegerField()
    experise = models.ForeignKey(Expertise, on_delete=models.CASCADE)


class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


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
