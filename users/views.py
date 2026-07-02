import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
# Create your views here.

from rest_framework import viewsets
from users.utils import validate_telegram_init_data
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from users.models import TelegramUser

@require_POST #using bare django for better understanding of api, easy to use api_view["POST"] with request.data
def user_jwt_generator(request):
    
    data = json.loads(request.body)
    init_data = data.get('init_data')
    
    validated_data = validate_telegram_init_data(init_data)
    
    if not validated_data:
        return JsonResponse({'status': 'Error'})
    
    user_info = validated_data.get('user')
    
    try:
        user, status = TelegramUser.objects.update_or_create(
        id=user_info.get('id'), 
        defaults={
            'username':user_info.get('username'), 
            'first_name':user_info.get('first_name')
            }
        )
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error'})
    
    refresh = RefreshToken.for_user(user)
    
    return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    return JsonResponse({
            'id':request.user.id,
            'username':request.user.username,
            'first_name': request.user.first_name
        })