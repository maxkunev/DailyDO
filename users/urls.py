from django.urls import path, include
from users import views

app_name = "users"

urlpatterns = [
    path('auth/telegram/', views.user_jwt_generator, name = "user_jwt_generator"),
    path('me/', views.get_user_info, name = 'get_user_info')    
]
 