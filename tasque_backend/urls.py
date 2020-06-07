"""tasque_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.authtoken import views

from tasque_rest.views import (TaskViewSet, ProjectViewSet,
    CustomFieldViewSet, HyperlinkResourceViewSet, MilestoneViewSet, login, Logout, VerifyToken)

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'customfields', CustomFieldViewSet)
router.register(r'resources', HyperlinkResourceViewSet)
router.register(r'milestones', MilestoneViewSet)

urlpatterns = [
    # path('tasque/', include('tasque_rest.urls')),
    path('admin/', admin.site.urls),
    #url('^/', include('django.contrib.auth.urls')),
    #path('login/', login, name='login'),
    url(r'^login/', views.obtain_auth_token),
    url(r'^logout/',  Logout.as_view()),
    url(r'^verify_token/', VerifyToken.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
