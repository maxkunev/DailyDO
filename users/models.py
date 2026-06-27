from django.db import models

# Create your models here.

class TelegramUser(models.Model):
    id = models.BigIntegerField(unique=True, blank=False, null=False, primary_key=True)
    username = models.CharField(blank=True, null=True, max_length=50)
    first_name = models.CharField(blank=True, null=True, max_length=50)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    