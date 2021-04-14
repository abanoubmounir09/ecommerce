from django.contrib import admin
from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_views
from .views import RegisterAPI
from rest_framework.authtoken.views import obtain_auth_token
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

urlpatterns = [
    # path('register',views.register,name="register"),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    
]

urlpatterns += [
    path('api-token-auth/', rest_views.obtain_auth_token)
]
