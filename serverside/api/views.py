from django.shortcuts import render
from rest_framework import generics
from . import serializers
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework import permissions
from . import permissions as custom_permissions
from .models import Profile, Charity

User = get_user_model()

# Create your views here.
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_auth(request):
    serialized = serializers.UserSerializer(data=request.data)
    print(serialized)
    if serialized.is_valid():
        User.objects.create_user(
            serialized.data['email'],
            serialized.data['username'],
            serialized.data['password']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([])
@permission_classes([])
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, custom_permissions.IsOwner])
class ReadUserAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, custom_permissions.IsOwnerOrReadOnly])
class ReadUpdateProfileAPIView(generics.RetrieveUpdateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            serializer_class = serializers.ProfileSerializer
        elif self.request.method == 'GET':
            serializer_class = serializers.ProfileReadSerializer
        elif self.request.method == 'PATCH':
            serializer_class = serializers.ProfileSerializer

        return serializer_class
    
    queryset = Profile.objects.all()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ListCharitiesAPIView(generics.ListAPIView):
    serializer_class = serializers.CharitySerializer
    queryset = Charity.objects.all()