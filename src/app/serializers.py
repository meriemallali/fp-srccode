from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['username', 'email',
                  'first_name', 'last_name', 'bio', 'photo', 'account_status', 'user_roles']


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManagement
        fields = '__all__'


class TeamsSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    team_list = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = TeamProject
        fields = ['team_name', 'created_by_username', 'created_by', 'team_list']


class ProjectTasksSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=ProjectManagement.objects.all())
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)

    class Meta:
        model = ProjectTasks
        fields = ['id', 'assigned_to', 'assigned_to_username', 'assigned_by', 'assigned_by_username',
                  'name', 'description',
                  'completed', 'project', 'project_name']
