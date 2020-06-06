from django.urls import include, path
from django.conf.urls import url, include

from rest_framework import routers

from .views import (TaskViewSet, UserViewSet, ProjectViewSet,
    CustomFieldViewSet, HyperlinkResourceViewSet, MilestoneViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'projects/(?P<project_id>.+)/tasks', TaskViewSet, basename='task')
router.register(r'customfields', CustomFieldViewSet)
router.register(r'resources', HyperlinkResourceViewSet)
router.register(r'milestones', MilestoneViewSet)

app_name = 'tasque_rest'
urlpatterns = [
    url(r'^', include(router.urls)),
]
