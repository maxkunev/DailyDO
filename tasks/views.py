from django.shortcuts import render
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your views here.
from tasks.models import Task
from rest_framework.views import APIView, Response

from tasks.serialaziers import TaskSerialazier
from users.authentication import JWTAuthenticationForCustomModel
from rest_framework.permissions import IsAuthenticated


class TasksAPIView(APIView): # Using APIView instead of ListCreateAPIView to understand better how api viewsets works
    authentication_classes = [JWTAuthenticationForCustomModel]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        instances = Task.objects.filter(user=request.user) # Insecure Direct Object Reference // to prevent other users from accessing confidential information
        
        target_date = request.query_params.get('date')
        
        if target_date: 
            try:
                instances = instances.filter(date=target_date)
            except ValidationError:
                instances = instances.none()
            
        serialazier_class = TaskSerialazier(instances, many=True)
        
        return Response(serialazier_class.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        
        serialazier_class = TaskSerialazier(data=request.data)
        
        if serialazier_class.is_valid():
            serialazier_class.save(user=request.user)
            return Response(serialazier_class.data, status=status.HTTP_201_CREATED)
        
        return Response(serialazier_class.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailAPIView(APIView): # Single Responsibility Principle
    authentication_classes = [JWTAuthenticationForCustomModel]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id, *args, **kwargs):
        try:
            instance = Task.objects.get(pk=id, user=request.user)
        except:
            return Response({'status': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serialazier_class = TaskSerialazier(instance)
        
        return Response(serialazier_class.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id, *args, **kwargs):
        try:
            instance = Task.objects.get(pk=id, user=request.user)
        except:
            return Response({'status': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serialazier_class = TaskSerialazier(instance, data=request.data, partial=True)
        
        if serialazier_class.is_valid():
            serialazier_class.save()
            return Response(serialazier_class.data, status=status.HTTP_200_OK)
        
        return Response(serialazier_class.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, *args, **kwargs):
        
        try:
            instance = Task.objects.get(pk=id, user=request.user)
        except:
            return Response({'status': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)      
        