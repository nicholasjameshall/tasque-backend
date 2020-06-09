from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login

from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import permission_classes

from .serializers import (CustomFieldSerializer, HyperlinkResourceSerializer,
    MilestoneSerializer, UserSerializer, TaskSerializer, ProjectSerializer)
from .models import Milestone, Task, Project, CustomField, HyperlinkResource

import json
from django.views.decorators.csrf import csrf_exempt
import logging


# Create your views here.
def index(request):
    return None

@csrf_exempt
def login(request):
    body = json.loads(request.body)
    username = body["username"]
    password = body["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        Token.objects.create(user=user)
        return JsonResponse({
            "result": "It worked!",
            "user": user.username
        }, status=200)
    else:
        return JsonResponse({
            "result": "Problem"
        }, status=401)

@permission_classes((permissions.AllowAny,))
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@permission_classes((permissions.AllowAny,))
class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@permission_classes((permissions.AllowAny,))
class VerifyToken(APIView):
    def get(self, request, format=None):
        user = request.user
        if user:
            return Response(status=status.HTTP_200_OK)
        Response(status=400)

def verify_token(request):
    if request.user:
        return JsonResponse({
            "result": "Logged in"
        }, status=200)
    else:
        return JsonResponse({
            "result": "User not logged in"
        }, status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomFieldViewSet(viewsets.ModelViewSet):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer

class HyperlinkResourceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = HyperlinkResource.objects.all()
    serializer_class = HyperlinkResourceSerializer

class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer

class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Task.objects.filter(user_id=user)


    """def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(pk=project_id)
        queryset = project.task_set.all()
        return queryset"""

class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    model = Project
    serializer_class = ProjectSerializer
    def get_queryset(self):
        domain = self.request.query_params.get('domain', None)
        user = self.request.user
        logger = logging.getLogger(__name__)
        logger.error(user)
        if domain and user.is_authenticated:
            return Project.objects.filter(user_id=user).filter(domain=domain)

        return Project.objects.all()
