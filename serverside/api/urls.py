from django.contrib import admin
from django.urls import path, include
from serverside.router import router
from rest_framework.authtoken import views as auth_views
from . import views
urlpatterns = [
    path('users/', views.UserCreateAPIView.as_view(), name='user-list'),
    path('users/login/', auth_views.obtain_auth_token),
    path('users/<int:pk>/', views.ReadUserAPIView.as_view()),
    path('users/<int:pk>/profile/', views.ReadUpdateProfileAPIView.as_view()),
    path('charities/', views.ListCharitiesAPIView.as_view())
]
