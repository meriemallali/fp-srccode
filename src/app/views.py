from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .forms import *
from .models import *
from .serializers import *
from itertools import chain
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


# url : 'signup'
# description : for users to create new account.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmedpassword = request.POST['confirmedpassword']
        # comparing the passwords, if match then check if user exists by email or username.
        # if not, register the new user and create its profile.
        if password == confirmedpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken, try with different one.')
                return redirect('signup')
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()
                # log user in
                logged_user = auth.authenticate(username=username, password=password)
                auth.login(request, logged_user)
                # create the profile for the new user
                new_userProfile = UserProfile.objects.create(user=User.objects.get(username=username))
                new_userProfile.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match. Re-enter password.')
            return redirect('signup')
    else:
        return render(
            request, 'signup.html')


# url : 'login'
# description: only registered users can sign in.
def signin_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        registered_user = authenticate(username=username, password=password)
        if registered_user:
            if registered_user.is_active:
                login(request, registered_user)
                return redirect('/')
            else:
                messages.info(request, 'Your account has been disabled.')
        else:
            messages.info(request, 'Invalid login details.')

    else:
        return render(request, 'login.html')

    return render(request, 'login.html')


# url: 'logout'
# description: only log in user can log out.
@login_required(login_url='login')
def logout_user(request):
    auth.logout(request)
    return redirect('login')


# url: ''
# @desc: dashboard to list statistic for the user.
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    # list the todos board based on their status. and order in descending based on created_at field.
    user_tasks = Task.objects.filter(user=user)
    not_started_tasks = Task.objects.filter(user=user, status='NOT STARTED').order_by('-created_at')
    in_progress_tasks = Task.objects.filter(user=user, status='IN PROGRESS').order_by('-created_at')
    completed_tasks = Task.objects.filter(user=user, status='DONE').order_by('-created_at')
    user_teams = TeamProject.objects.filter(team_list=request.user)
    # Retrieve projects associated with user's teams and order in descending based on created_at field.
    user_projects = ProjectManagement.objects.filter(team__in=user_teams).order_by('-created_at')
    user_project_tasks = ProjectTasks.objects.filter(assigned_to=user)
    project_tasks_notcompleted = ProjectTasks.objects.filter(assigned_to=user, completed=False)
    project_tasks_completed = ProjectTasks.objects.filter(assigned_to=user, completed=True)
    p_tasksnotcompleted_total = len(project_tasks_notcompleted)
    p_taskscompleted_total = len(project_tasks_completed)
    project_total = len(user_projects)
    if len(user_tasks) == 0:
        productivity_rate = 0
    else:
        productivity_rate = round((len(completed_tasks) / len(user_tasks)) * 100)
    if len(user_project_tasks) == 0:
        overall_completion_rate = 0
    else:
        overall_completion_rate = round((p_taskscompleted_total / len(user_project_tasks)) * 100)
    context = {
        'user_profile': user_profile,
        'not_started_tasks': len(not_started_tasks),
        'in_progress_tasks': len(in_progress_tasks),
        'completed_tasks': len(completed_tasks),
        'productivity_rate': productivity_rate,
        'project_total': project_total,
        'p_tasksnotcompleted_total': p_tasksnotcompleted_total,
        'p_taskscompleted_total': p_taskscompleted_total,
        'completion_rate': overall_completion_rate

    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
# url: /profile/settings
# @desc: users can edit their profile
def profile_settings(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        if request.FILES.get('photo') is None:
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            bio = request.POST['bio']
            profile_photo = user_profile.photo
            user_profile.first_name = firstname
            user_profile.last_name = lastname
            user_profile.bio = bio
            user_profile.photo = profile_photo
            user_profile.save()
        elif request.FILES.get('photo') is not None:
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            bio = request.POST['bio']
            profile_photo = request.FILES.get('photo')
            user_profile.first_name = firstname
            user_profile.last_name = lastname
            user_profile.bio = bio
            user_profile.photo = profile_photo
            user_profile.save()
        return redirect('/profile/settings')

    return render(request, 'settings.html', {'user_profile': user_profile})


# url: /tasks
# @desc: users can create todos
@login_required(login_url='login')
def create_task(request):
    user = request.user
    # list the todos board based on their status. and order in descending based on created_at field. 
    not_started = Task.objects.filter(user=user, status='NOT STARTED').order_by('-created_at')
    in_progress = Task.objects.filter(user=user, status='IN PROGRESS').order_by('-created_at')
    completed = Task.objects.filter(user=user, status='DONE').order_by('-created_at')

    if request.method == "POST":
        # creating new task:
        task_content = request.POST['content']
        new_task = Task.objects.create(user=user, content=task_content)
        new_task.save()

        return redirect("tasks")
    # Retrieve the user profile.
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
        'not_started_tasks': not_started,
        'in_progress_tasks': in_progress,
        'done_tasks': completed,
    }

    return render(request, 'todo.html', context)


# url : 'edit_task/<int:task_id>/'
# @desc: edit the created todos.
@login_required(login_url='login')
def edit_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.select_for_update().filter(pk=task_id).first()
        if task:
            new_content = request.POST.get('new_content')
            task.content = new_content
            task.save()
            return redirect('tasks')  # Redirect  after saving changes
        else:
            return redirect('tasks')  # Redirect if task is not found
    else:
        return redirect('tasks')  # Redirect if request method is not POST


# URL: 'complete/<int:task_id>/'
# @desc: Mark task as completed
@login_required(login_url='login')
def complete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.filter(pk=task_id).first()
        if task:
            task.status = 'DONE'
            task.save()
            return redirect('tasks')
    return redirect('tasks')


# URL: 'in-progress/<int:task_id>/'
# @desc: Mark task as in progress
@login_required(login_url='login')
def in_progress_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.filter(pk=task_id).first()
        if task:
            task.status = 'IN PROGRESS'
            task.save()
            return redirect('tasks')
    return redirect('tasks')


# url: /delete_todo/<int:pk>/
# @desc: users can deleted created todos
@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    context = {
        'task': task,
    }
    return render(request, 'todo.html', context)


# url: "/myprojects/
# @desc: display all projects related to the logged-in user
@login_required(login_url='login')
def my_projects(request):
    user_teams = TeamProject.objects.filter(team_list=request.user)
    # Retrieve projects associated with user's teams and order in descending based on created_at field.
    user_projects = ProjectManagement.objects.filter(team__in=user_teams).order_by('-created_at')
    # Get team list associated with each project.
    project_data = []
    for project in user_projects:
        project_detail = {
            'project': project,
            'team_name': project.team.team_name,
            'team_list': project.team.team_list.all()
        }
        project_data.append(project_detail)

    # Retrieve the user profile.
    user_profile = UserProfile.objects.get(user=request.user)
    user = request.user
    # Get all teams and users for the control panel.
    team_list = TeamProject.objects.all()
    users_list = User.objects.all()
    # Get all project tasks for the user.
    user_tasks = []
    assigned_tasks = ProjectTasks.objects.filter(assigned_to=user)
    if assigned_tasks or user_projects:
        for project in user_projects:
            try:
                project_task_user = ProjectTasks.objects.filter(project=project, assigned_to=user)
                user_tasks.append(project_task_user)
            except ProjectTasks.DoesNotExist:
                pass
    projects = ProjectManagement.objects.all()
    context = {
        'user_profile': user_profile,
        'team_list': team_list,
        'users_list': users_list,
        'project_tasks': user_tasks,
        'project_data': project_data,
        'projects': projects
    }

    return render(request, 'my_projects.html', context)


# url: "/projects/project_details/<int:project_id>/"
# @desc: display the details of the selected project.
@login_required(login_url='login')
def project_details(request, project_id):
    user = request.user
    project = ProjectManagement.objects.get(id=project_id)
    project_tasks = ProjectTasks.objects.filter(project=project, assigned_to=user)
    # if user is == project manager or admin or lead render all the project tasks
    project_tasks_all = ProjectTasks.objects.filter(project=project)
    user_profile = UserProfile.objects.get(user=user)
    len_of_tasks = len(project_tasks_all)
    data = {'project': project,
            'project_tasks': project_tasks,
            'project_tasks_all': project_tasks_all,
            'user_profile': user_profile,
            'number_of_tasks': len_of_tasks,
            }

    return render(request, 'project_detail.html', data)


# url: "/create_project/"
# @desc: only users with roles:  [admin or project manager or lead] can create a new project.
@login_required(login_url='login')
def create_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        description = request.POST.get('description')
        created_by = request.user
        team_id = request.POST.get('team_id')
        team = TeamProject.objects.get(pk=team_id)
        new_project = ProjectManagement.objects.create(project_name=project_name, description=description,
                                                       created_by=created_by, team=team)

        new_project.save()
        return redirect('my_projects')
    return redirect('my_projects')


# url:'myprojects/create_ptask/'
# @desc: only users with roles:  [admin or project manager or lead] can create a new project task.
@login_required(login_url='login')
def create_ptask(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = ProjectManagement.objects.get(id=project_id)
        name = request.POST.get('taskp_name')
        description = request.POST.get('taskp_description')
        assigned_by = request.user
        assigned_to_id = request.POST.get('taskp_assigned_to')
        assigned_to_user = User.objects.get(id=assigned_to_id)
        completed = False
        new_ptask = ProjectTasks.objects.create(project=project, name=name, description=description,
                                                assigned_by=assigned_by, assigned_to=assigned_to_user,
                                                completed=completed)
        new_ptask.save()

    return redirect('my_projects')


# url:'myprojects/delete_ptask/<int:ptask_id>'
# @desc: only users with roles:  [admin or project manager or lead] can delete a project task.
@login_required(login_url='login')
def delete_ptask(request, ptask_id, project_id):
    project_task = get_object_or_404(ProjectTasks, pk=ptask_id)
    if request.method == 'POST':
        project_task.delete()
        return redirect(reverse('project_details', args=[project_id]))


# url: 'myprojects/edit_ptask/<int:ptask_id>/<int:project_id>'
# @desc: only users with roles:  [admin or project manager or lead] can edit a project task.
@login_required(login_url='login')
def edit_ptask(request, ptask_id, project_id):
    project_task = get_object_or_404(ProjectTasks, pk=ptask_id)
    if request.method == 'POST':
        name = request.POST.get('task_name')
        description = request.POST.get('task_description')
        project_task.name = name
        project_task.description = description
        project_task.save()
        return redirect(reverse('project_details', args=[project_id]))


# url:'myprojects/toggle_task/<int:task_id>/'
# @desc: mark project task as completed.
@login_required(login_url='login')
def mark_project_task(request, task_id):
    _task = ProjectTasks.objects.get(id=task_id)
    project_id = _task.project.id
    if request.method == 'POST':
        toggle_task = request.POST.get('toggle_task')
        _task.completed = toggle_task
        _task.save()
    return redirect(reverse('project_details', args=[project_id]))


# url : "myprojects/delete_project/<int:project_id>/"
# @desc: only users with roles: [admin or project manager or lead] can delete a project.
@login_required(login_url='login')
def delete_project(request, project_id):
    project = get_object_or_404(ProjectManagement, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect(reverse('my_projects'))


# url: 'myprojects/edit_project/<int:project_id>/'
# @desc: only users with roles: [admin or project manager or lead] can edit a project.
@login_required(login_url='login')
def edit_project(request, project_id):
    project = ProjectManagement.objects.get(id=project_id)
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        description = request.POST.get('project_description')
        project.project_name = project_name
        project.description = description
        project.save()

    return redirect(reverse('my_projects'))


# url : "myprojects/create_team/"
# @desc: only users with roles: [admin or project manager or lead] can create a new team and assign members to a team.
@login_required(login_url='login')
def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        team_member_id = request.POST.getlist('user_ids')
        team_member = User.objects.filter(id__in=team_member_id)
        print(team_member)
        if team_name:
            new_team = TeamProject.objects.create(team_name=team_name, created_by=request.user)
            new_team.team_list.add(*team_member)
            new_team.save()
            return redirect('my_projects')
    return redirect('my_projects')


# url: "myprojects/add_member/"
# @desc: only users with roles: [admin or project manager or lead] can assign a member to a team.
@login_required(login_url='login')
def add_member(request):
    if request.method == 'POST':
        # push a member to an existing team.
        team_id = request.POST.get('team_id')
        team = get_object_or_404(TeamProject, pk=team_id)
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        team.team_list.add(user)
        return redirect('my_projects')

    return redirect('my_projects')


# url: 'chat/direct_chat/<int:id>/<str:room_name>'
# @desc: direct messaging between users.
@login_required(login_url='login')
def direct_chat(request, id, room_name):
    user = request.user
    users_profiles = UserProfile.objects.all()
    user_profile = UserProfile.objects.get(user=user)
    sent_to_user = User.objects.get(username=room_name)
    messages_sent = DmChat.objects.filter(sent_by=user, sent_to=sent_to_user)
    messages_received = DmChat.objects.filter(sent_by=sent_to_user, sent_to=user)
    chat_history = list(messages_sent) + list(messages_received)
    chat_history_sorted = sorted(chat_history, key=lambda x: x.timestamp)
    selected_profile = UserProfile.objects.get(user=sent_to_user)

    context = {
        'user_profile': user_profile,
        'users_profiles': users_profiles,
        'receiver': sent_to_user.id,
        'selected_profile': selected_profile,
        'chat_username': sent_to_user.username,
        'chat_history': chat_history_sorted,
        'user_id': user.id,
    }
    return render(request, 'dm-chat.html', context)


# url: 'api/user_data'
class UserDataAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


# url: 'api/projects'
class ProjectsAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectsSerializer
    queryset = ProjectManagement.objects.all()


# url: 'api/teams'
class TeamsAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamsSerializer
    queryset = TeamProject.objects.all()


# url: 'api/projects_tasks'
class ProjectTasksAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectTasksSerializer
    queryset = ProjectTasks.objects.all()
