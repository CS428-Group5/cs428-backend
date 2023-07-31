from django.db import models
from users.models import Mentee, MentorSession

# Create your models here.
class Session(models.Model):
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    mentor_session = models.OneToOneField(MentorSession, on_delete=models.CASCADE)
    event_id = models.TextField()
    CANCELED_BY_CHOICES = (
        (None, "Not canceled"),
        (1, "Mentor canceled"),
        (2, "Mentee canceled")
    )
    cancelled_by = models.SmallIntegerField(
        choices= CANCELED_BY_CHOICES,
        default=None
    )

    def save(self, *arg, **kwargs):
        if self.cancelled_by == 1 and Session.objects.filter(id=self.id, cancelled_by=2):
            raise ValueError("A mentor has already canceled this session. A mentee cannot cancel it now")
        elif self.cancelled_by == 2 and Session.objects.filter(id=self.id, cancelled_by=1):
            raise ValueError("A mentee has already canceled this session. A mentor cannot cancel it now.")
        return super().save(*arg, **kwargs)
