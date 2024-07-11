from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_api(request):
    user = request.user
    return Response({'message': f'Welcome, {user.username}!'})

@api_view(['GET'])
def login_api(request):
    return redirect(reverse('social:begin', args=['facebook']))