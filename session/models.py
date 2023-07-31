from django.db import models
from users.models import Mentee, Mentor

# Create your models here.
class MentorSession(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    session_time = models.TimeField()
    session_date = models.DateField()
    is_book = models.BooleanField(default=False)

class BookedSession(models.Model):
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    mentor_session = models.ForeignKey(MentorSession, on_delete=models.CASCADE)
    event_id = models.TextField()
    CANCELED_BY_CHOICES = (
        (0, "Not canceled"),
        (1, "Mentor canceled"),
        (2, "Mentee canceled")
    )
    cancelled_by = models.SmallIntegerField(
        choices= CANCELED_BY_CHOICES,
        default=0
    )

    def save(self, *arg, **kwargs):
        if self.cancelled_by == 1 and BookedSession.objects.filter(id=self.id, cancelled_by=2):
            raise ValueError("A mentor has already canceled this session. A mentee cannot cancel it now")
        elif self.cancelled_by == 2 and BookedSession.objects.filter(id=self.id, cancelled_by=1):
            raise ValueError("A mentee has already canceled this session. A mentor cannot cancel it now.")
        return super().save(*arg, **kwargs)
