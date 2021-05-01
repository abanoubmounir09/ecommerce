from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
import json
from rest_framework.response import Response
from django.contrib.auth import views as auth_views
from .serializers import userSerializer
from django.contrib import auth

from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework import serializers

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer


from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print("request.data++++++++++++++++++",request.data)
        # print("serializer++++++++++++++++++",serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if request.data['is_staff'] == "true":
            user.is_staff=True 
            user.save()
        login(request, user)
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        print("*****AuthTokenSerializer///////---",serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        activeuser=User.objects.get(username=user.username)
        datatest={}
        datatest['is_staff']=activeuser.is_staff
        login(request, user)
        temp_list=super(LoginAPI, self).post(request, format=None)
        temp_list.data["is_staff"]=activeuser.is_staff
        temp_list.data["email"]=activeuser.email
        temp_list.data["id"]=activeuser.pk
        temp_list.data["username"]=activeuser.username
        temp_list.data["last_login"]=activeuser.last_login
        return Response({"data":temp_list.data})








































#-----------------------------------------
"""
#register2 user new as docmentation
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serialzer=userSerializer(data=request.data)
        data={}
        if serialzer.is_valid():
            userOb=serialzer.save()

            data['response']="successfully register user"
            data['username']=userOb.username
            data['email']=userOb.email
            #token-------------------
            token = Token.objects.create(user=userOb)
            print("tokeni in register view",token.key)
            getToken=Token.objects.get(user=userOb).key
            data["token"]=getToken
            test=serialzer.data['username']
            login(request,test)

        else:
            data= serialzer.errors
        return Response(data)

"""
"""
#register user from angualr
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        username1=body['UserName']
        email=body['Email']
        password1=body['Password']
        password2=body['ConfirmPassword']
        newUser=User.objects.create_user(username=username1,email=email,password=password1)
        newUser.save()
        token = Token.objects.create(user=newUser)
        print("tokeni in register view",token.key)
        newUser = authenticate(username=username1, password=password1)
        if newUser is not None:
            # login(request,userauth)
            login(request,newUser)
            print("username in loogin",request.user.username)
            return Response(body)
        else:
            return HttpResponse("not loggin user in register func")

 """       
        

 







