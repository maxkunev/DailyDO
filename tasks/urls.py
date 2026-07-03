from django.urls import path, include
from tasks.views import TasksAPIView, TaskDetailAPIView 

app_name = "tasks"

urlpatterns = [
    path('tasks/', TasksAPIView.as_view(), name='api-tasks'),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view(), name='api-task')
]
