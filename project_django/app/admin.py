from django.contrib import admin
from .models import Project, Task, File, Milestone, ProgressReport, Notification, PriorityLevel

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(File)
admin.site.register(Milestone)
admin.site.register(ProgressReport)
admin.site.register(Notification)
admin.site.register(PriorityLevel)