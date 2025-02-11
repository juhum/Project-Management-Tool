from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(User)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/projects/{self.pk}/'

class PriorityLevel(models.Model):
    level = models.CharField(max_length=20)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    priority_level = models.ForeignKey(PriorityLevel, on_delete=models.CASCADE)
    deadline = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class File(models.Model):
    pass
    # file = models.FileField(upload_to='files/')
    # uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Notification(models.Model):
    message = models.TextField()
    recipients = models.ManyToManyField(User) 
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)


def project_file_path(instance, filename):
    return f'project_files/project_{instance.project.id}/{filename}'

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to=project_file_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


