from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from users.models import TelegramUser

class JWTAuthenticationForCustomModel(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('user_id')
            user = TelegramUser.objects.get(pk=user_id)
        except Exception as e:
            raise AuthenticationFailed(
                ("User not found"), code="user_not_found"
            ) from e
        
        return user
