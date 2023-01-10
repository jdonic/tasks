from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def mark_completed(self) -> None:
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()
