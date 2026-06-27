from django.db import models

# Create your models here.

from users.models import TelegramUser

class Task(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="tasks")
    text = models.TextField()
    date = models.DateField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    