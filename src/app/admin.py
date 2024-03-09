from django.contrib import admin
from .models import *

# Registering the created models into the admin site.
admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(ProjectManagement)
admin.site.register(ProjectTasks)
admin.site.register(TeamProject)
admin.site.register(DmChat)
