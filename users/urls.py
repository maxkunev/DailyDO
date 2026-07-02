from django.urls import path, include
from users import views

urlpatterns = [
    path('api/auth/telegram/', views.user_jwt_generator, name = "user_jwt_generator"),
    path('api/me/', views.get_user_info, name = 'get_user_info')    
]
 