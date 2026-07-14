from django.db import models
from django.core.validators import MaxLengthValidator
# Create your models here.

from users.models import TelegramUser

class Task(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="tasks")
    text = models.TextField(validators=[MaxLengthValidator(300)])
    date = models.DateField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    