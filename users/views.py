from datetime import datetime, timedelta, timezone
import json
from django.utils import timezone as d_timezone

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
# Create your views here.

from rest_framework import viewsets
from users.utils import validate_telegram_init_data
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from django.views.decorators.csrf import csrf_exempt

from users.models import TelegramUser

@csrf_exempt
@require_POST #using bare django for better understanding of api, easy to use api_view["POST"] with request.data
def user_jwt_generator(request):
    
    try:
        data = json.loads(request.body)
        init_data = data.get('initData')
        
        if not init_data:
                return JsonResponse({'error': 'no initData provided'}, status=400)
        
        validated_data = validate_telegram_init_data(init_data)
        
        if not validated_data:
            return JsonResponse({'status': 'invalid signature'}, status=401)
        
        auth_date = validated_data.get('auth_date', {})
        
        if not auth_date:
            return JsonResponse({'status': 'auth_date missing'}, status=401)
        
        try:
            auth_date = datetime.fromtimestamp(int(auth_date), tz=timezone.utc)
        except:
            return JsonResponse({'status': 'invalid auth_date'}, status=401)
        
        if d_timezone.now() - auth_date > timedelta(minutes=60):
            return JsonResponse({'status': 'InitData expired'}, status=401)
        
        user_info_str = validated_data.get('user', None)
        user_info = json.loads(user_info_str)
        
        try:
            user, status = TelegramUser.objects.update_or_create(
            id=user_info.get('id'), 
            defaults={
                'username':user_info.get('username'), 
                'first_name':user_info.get('first_name')
                }
            )
        except Exception as e:
            import traceback
            print('FULL ERROR:')
            traceback.print_exc()
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
        
        refresh = RefreshToken.for_user(user)
        
        return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
            
            
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    return JsonResponse({
            'id':request.user.id,
            'username':request.user.username,
            'first_name': request.user.first_name,
            'language': request.user.language
        })