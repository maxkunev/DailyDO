from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    
    list_display = ("id", "user", "created_at")
    search_fields = ["id"]

admin.site.register(Task, TaskAdmin)