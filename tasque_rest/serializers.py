from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Milestone, Task, Project, CustomField, HyperlinkResource

class MilestoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Milestone
        fields = ['name']

class CustomFieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomField
        fields = ['name', 'value']

class HyperlinkResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HyperlinkResource
        fields = ['task_id', 'name', 'hyperlink']

class TaskSerializer(serializers.ModelSerializer):
    custom_fields = CustomFieldSerializer(source='customfield_set', many=True, allow_null=True, required=False)
    resources = HyperlinkResourceSerializer(source='hyperlinkresource_set', many=True, allow_null=True, required=False)
    class Meta:
        model = Task
        fields = ['id', 'priority', 'description', 'start_date', 'end_date', 'status', 'custom_fields', 'resources', 'project_id']

    def create(self, validated_data):
        user = self.context['request'].user
        return Task.objects.create(**validated_data, user_id=user)

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="project-detail")
    tasks = TaskSerializer(source='task_set', many=True, allow_null=True, required=False)
    milestones = MilestoneSerializer(source='milestone_set', many=True, allow_null=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'domain', 'url', 'name', 'start_date', 'end_date', 'tasks', 'milestones']

    def create(self, validated_data):
        user = self.context['request'].user
        return Project.objects.create(**validated_data, user_id=user)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
