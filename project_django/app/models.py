from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    team_members = models.ManyToManyField(User)  # Use Djoser's User model
    # not sure if these methods needed later
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
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Djoser's User model
    priority_level = models.ForeignKey(PriorityLevel, on_delete=models.CASCADE)
    deadline = models.DateField()
    status = models.CharField(max_length=50)

class File(models.Model):
    file = models.FileField(upload_to='files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Djoser's User model
    uploaded_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Milestone(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=50)

class ProgressReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    progress_percentage = models.PositiveIntegerField()
    notes = models.TextField()
    date = models.DateField()

class Notification(models.Model):
    message = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Djoser's User model
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


def project_file_path(instance, filename):
    return f'project_files/project_{instance.project.id}/{filename}'

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to=project_file_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

