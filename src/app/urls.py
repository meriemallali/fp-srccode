from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user_data', UserDataAPI)
router.register(r'projects', ProjectsAPI)
router.register(r'teams', TeamsAPI)
router.register(r'projects_tasks', ProjectTasksAPI)

urlpatterns = [
    path('login', signin_user, name="login"),
    path('signup', register, name="signup"),
    path('logout', logout_user, name="logout"),
    path('', dashboard, name="dashboard"),
    path('tasks/', create_task, name='tasks'),
    # urls for personal tasks.
    path('edit_task/<int:task_id>/', edit_task, name='edit_task'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('in_progress_task/<int:task_id>/', in_progress_task, name='in_progress_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    # urls for projects.
    path('myprojects/', my_projects, name='my_projects'),
    path('myprojects/project_details/<int:project_id>/', project_details, name='project_details'),
    path('myprojects/create_project/', create_project, name='create_project'),
    path('myprojects/create_team/', create_team, name='create_team'),
    path('myprojects/add_member/', add_member, name='add_member'),
    path('myprojects/delete_project/<int:project_id>/', delete_project, name='delete_project'),
    path('myprojects/edit_project/<int:project_id>/', edit_project, name='edit_project'),
    # create project task
    path('myprojects/create_ptask/', create_ptask, name='create_ptask'),
    path('myprojects/delete_ptask/<int:ptask_id>/<int:project_id>', delete_ptask, name='delete_ptask'),
    path('myprojects/edit_ptask/<int:ptask_id>/<int:project_id>', edit_ptask, name='edit_ptask'),
    # toggle project task.
    path('myprojects/toggle_task/<int:task_id>/', mark_project_task, name='toggle_task'),
    # urls for user profile.
    path('profile/settings', profile_settings, name='settings'),
    # urls for real-time chat.
    path('chat/direct_chat/<int:id>/<str:room_name>', direct_chat, name='direct_chat'),
    # include rest api urls
    path('api/', include(router.urls)),
]
