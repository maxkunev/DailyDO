from django.contrib import admin
from .models import Tasks
# Register your models here.

class TasksAdmin(admin.ModelAdmin):
    
    list_display = ("id", "user", "created_at")
    search_fields = ["id"]

admin.site.register(Tasks, TasksAdmin)