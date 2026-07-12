from django.urls import path, include
from users import views

from rest_framework_simplejwt.views import TokenRefreshView

app_name = "users"

urlpatterns = [
    path('auth/telegram/', views.user_jwt_generator, name = "user_jwt_generator"),
    path('me/', views.get_user_info, name = 'get_user_info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')    
]
 