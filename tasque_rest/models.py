from django.db import models
from django.contrib.auth.models import User

STATUSES = [
    ('new', 'New'),
    ('taken', 'Taken'),
    ('completed', 'Completed'),
    ('deleted', 'Deleted')
]

DOMAINS = [
    ('personal', 'Personal'),
    ('work', 'Work')
]

class Project(models.Model):
    def __str__(self):
        return self.name

    user_id = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True
        )
    domain = models.CharField(choices=DOMAINS, default='personal', max_length=10)
    name = models.CharField(max_length=25)
    last_updated = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    # Foreign keys:
    #   Task
    #   Milestone

class Task(models.Model):
    def __str__(self):
        return self.description

    project_id = models.ForeignKey(
            Project,
            on_delete=models.CASCADE
        )
    user_id = models.ForeignKey(
            User,
            on_delete=models.CASCADE
        )
    priority = models.IntegerField()
    description = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=STATUSES, default='new', max_length=10)
    comment = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['start_date']

    # Foreign keys:
    #   CustomField
    #   HyperlinkResource

class CustomField(models.Model):
    def __str__(self):
        return self.name

    task_id = models.ForeignKey(
            Task,
            on_delete=models.CASCADE,
            null=True,
            blank=True
        )
    name = models.CharField(max_length=50)
    value = models.FloatField()

class HyperlinkResource(models.Model):
    def __str__(self):
        return self.name

    task_id = models.ForeignKey(
            Task,
            on_delete=models.CASCADE,
            null=True,
            blank=True
        )
    name = models.CharField(max_length=50)
    hyperlink = models.CharField(max_length=200)

class Milestone(models.Model):
    def __str__(self):
        return self.name

    project_id = models.ForeignKey(
            Project,
            on_delete=models.SET_NULL,
            null=True
        )
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
