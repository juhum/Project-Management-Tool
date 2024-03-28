from django.contrib import admin
from .models import Project, Task, File, Notification, PriorityLevel, ProjectFile, Status

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(File)
admin.site.register(Notification)
admin.site.register(PriorityLevel)
admin.site.register(ProjectFile)
admin.site.register(Status)