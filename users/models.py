from django.db import models

# Create your models here.

class TelegramUser(models.Model):
    
    class Language(models.TextChoices):
        ENGLISH = "en", "English"
        RUSSIAN = "ru", "Russian"
        UKRAINIAN = "uk", "Ukrainian"

    id = models.BigIntegerField(blank=False, null=False, primary_key=True)
    chat_id = models.BigIntegerField(null=True, blank=True)
    username = models.CharField(blank=True, null=True, max_length=50)
    first_name = models.CharField(blank=True, null=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    language = models.CharField(max_length=2, default=Language.ENGLISH, choices=Language.choices)
    
    @property
    def is_authenticated(self):
        return True