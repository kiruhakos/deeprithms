from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import filters
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .forms import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from djoser.serializers import TokenSerializer
from rest_framework import permissions, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

User = get_user_model()

class RegisterAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main")
        return render(request, 'main/register.html')
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = Profile.objects.create(user=user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        login(request, user)
        return redirect("main")

class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main")
        return render(request, 'main/login.html')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        serializer = serializers.UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        login(request, user)

        if user.socialaccount_set.filter(provider='github').exists() and user.socialaccount_set.filter(provider='google').exists():
            profile, created = Profile.objects.get_or_create(user=user)

        return redirect("main")

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logout(request)
                return redirect("main")
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            logout(request)
            return redirect("main")
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class NewPasswordAPIView(UpdateAPIView):
    serializer_class = NewPasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return render(request, 'main/new-password.html')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
        
            if not self.object.check_password(old_password):
                message_tags = messages.get_messages(request)
                messages.error(request, _('Wrong password.'))
                return render(request, 'main/new-password.html', {'message_tags': message_tags})

            self.object.set_password(new_password)
            self.object.save()
            login(request, user)
            return redirect("main")

        return render(request, 'main/new-password.html', {'errors': serializer.errors})


class UserAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user

from rest_framework_simplejwt.authentication import JWTAuthentication

class LoadMoreProjects(View):
    def get(self, request):
        page_number = request.GET.get('page')
        projects = Project.objects.order_by('-posted')
        paginator = Paginator(projects, 2) 
        page_obj = paginator.get_page(page_number)

        project_data = []
        for project in page_obj:
            project_data.append({
                'title': project.title,
                'info': project.info,
                'posted': project.posted,
                'colab': project.colab
            })

        return JsonResponse({
            'projects': project_data,
            'has_next': page_obj.has_next()
        })


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    
    def get(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        projects = Project.objects.filter(user=profile).order_by('-posted')
        paginator = Paginator(projects, 2) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = ProfileSerializer(profile)
        return render(request, 'main/profile.html', {'profile': profile, 'projects': page_obj})

    def post(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        if int(request.user.id) == id:
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.validated_data:
                    serializer.validated_data['user'] = request.user 
                    serializer.save()
                    return redirect("profile", id=profile.id)
                else: 
                    return redirect("profile", id=profile.id)
            else: 
                print(serializer.errors)
            return render(request, 'main/profile.html', {'profile': profile, 'serializer': serializer})
        else: 
            return HttpResponse('Unauthorized', status=401)
