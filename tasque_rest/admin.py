from django.contrib import admin

from django.contrib.auth.models import User
from .models import Project, Task, CustomField, HyperlinkResource, Milestone

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(CustomField)
admin.site.register(HyperlinkResource)
admin.site.register(Milestone)
