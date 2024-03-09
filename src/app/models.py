from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# User Profile model
# To store user's data.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile/', default='blankprofile.jpg', null=True)
    account_status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='active')
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    user_roles = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('project manager', 'Project Manager'),
        ('lead', 'Lead')
    ], null=True, blank=True)

    def __str__(self):
        return self.user.username


# To store created todos.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = (
        ('NOT STARTED', 'Not started '), ('IN PROGRESS', 'In Progress'),
        ('DONE', 'Done'))
    status = models.CharField(max_length=20, choices=status_choices, default='NOT STARTED')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.content


# To manage teams.
class TeamProject(models.Model):
    team_name = models.CharField(max_length=255)
    team_list = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_name


# To manage projects.
class ProjectManagement(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True, max_length=400)
    created_by = models.ForeignKey(User, related_name='created_project', on_delete=models.CASCADE)
    team = models.ForeignKey(TeamProject, related_name='projects', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.project_name


# To manage the tasks within a project.
class ProjectTasks(models.Model):
    project = models.ForeignKey(ProjectManagement, on_delete=models.CASCADE, related_name='project_tasks')
    name = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='assigned_to_task', on_delete=models.CASCADE, null=True)
    assigned_by = models.ForeignKey(User, related_name='assigned_by_task', on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.project}"


# To manage direct messaging.
class DmChat(models.Model):
    content = models.TextField()
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_dm')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_dm')
    chat_name = models.CharField(blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f" from {self.sent_by} to {self.sent_to}"

