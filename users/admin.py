from django.contrib import admin
from .models import TelegramUser
# Register your models here.

class TelegramUserAdmin(admin.ModelAdmin):
    
    list_display = ("id", "username", "created_at")
    search_fields = ["id"]

admin.site.register(TelegramUser, TelegramUserAdmin)