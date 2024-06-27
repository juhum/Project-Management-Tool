from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Project, Task, File, Notification, PriorityLevel, ProjectFile, Status
import os
from django.core.files.uploadedfile import SimpleUploadedFile

class ProjectTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.status = Status.objects.create(name='In Progress')
        self.project = Project.objects.create(
            title='Test Project',
            description='Project description',
            start_date='2024-01-01',
            end_date='2024-12-31',
            status=self.status
        )
        self.project.team_members.add(self.user)
        self.client.force_authenticate(user=self.user)
    
    def test_get_projects(self):
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_project(self):
        data = {
            'title': 'New Project',
            'description': 'New description',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'status': self.status.id,
            'team_members': [self.user.id]
        }
        response = self.client.post(reverse('project-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_get_project_detail(self):
        response = self.client.get(reverse('project-detail', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.project.title)

    def test_update_project(self):
        data = {
            'title': 'Updated Project',
            'description': 'Updated description',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'status': self.status.id,
            'team_members': [self.user.id]
        }
        response = self.client.put(reverse('project-detail', kwargs={'pk': self.project.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project')

    def test_delete_project(self):
        response = self.client.delete(reverse('project-detail', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

class TaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Project.objects.create(
            title='Test Project',
            description='Project description',
            start_date='2024-01-01',
            end_date='2024-12-31',
            status=Status.objects.create(name='In Progress')
        )
        self.priority_level = PriorityLevel.objects.create(level='High')
        self.task = Task.objects.create(
            title='Test Task',
            description='Task description',
            project=self.project,
            assigned_to=self.user,
            priority_level=self.priority_level,
            deadline='2024-06-30',
            status=Status.objects.create(name='Not Started')
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_tasks(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'New description',
            'project': self.project.id,
            'assigned_to': self.user.id,
            'priority_level': self.priority_level.id,
            'deadline': '2024-06-30',
            'status': Status.objects.create(name='In Progress').id
        }
        response = self.client.post(reverse('task-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_task_detail(self):
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'project': self.project.id,
            'assigned_to': self.user.id,
            'priority_level': self.priority_level.id,
            'deadline': '2024-06-30',
            'status': Status.objects.create(name='Completed').id
        }
        response = self.client.put(reverse('task-detail', kwargs={'pk': self.task.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.delete(reverse('task-detail', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

class FileTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Project.objects.create(
            title='Test Project',
            description='Project description',
            start_date='2024-01-01',
            end_date='2024-12-31',
            status=Status.objects.create(name='In Progress')
        )
        self.file = File.objects.create(
            file=SimpleUploadedFile("file.txt", b"file_content"),
            uploaded_by=self.user,
            project=self.project
        )
        self.client.force_authenticate(user=self.user)

    def test_get_files(self):
        response = self.client.get(reverse('file-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_file(self):
        with open('temp_file.txt', 'w') as f:
            f.write('temporary file content')
        
        with open('temp_file.txt', 'rb') as f:
            data = {
                'file': f,
                'uploaded_by': self.user.id,
                'project': self.project.id
            }
            response = self.client.post(reverse('file-list'), data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(File.objects.count(), 2)

        os.remove('temp_file.txt')

    def test_get_file_detail(self):
        response = self.client.get(reverse('file-detail', kwargs={'pk': self.file.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file'], self.file.file.url)

    def test_update_file(self):
        with open('temp_file.txt', 'w') as f:
            f.write('updated temporary file content')
        
        with open('temp_file.txt', 'rb') as f:
            data = {
                'file': f,
                'uploaded_by': self.user.id,
                'project': self.project.id
            }
            response = self.client.put(reverse('file-detail', kwargs={'pk': self.file.id}), data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        os.remove('temp_file.txt')

    def test_delete_file(self):
        response = self.client.delete(reverse('file-detail', kwargs={'pk': self.file.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(File.objects.count(), 0)

class NotificationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Project.objects.create(
            title='Test Project',
            description='Project description',
            start_date='2024-01-01',
            end_date='2024-12-31',
            status=Status.objects.create(name='In Progress')
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Task description',
            project=self.project,
            assigned_to=self.user,
            priority_level=PriorityLevel.objects.create(level='High'),
            deadline='2024-06-30',
            status=Status.objects.create(name='Not Started')
        )
        self.notification = Notification.objects.create(
            message='Test notification',
            read=False,
            project=self.project,
            task=self.task
        )
        self.notification.recipients.add(self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_notifications(self):
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_notification(self):
        data = {
            'message': 'New notification',
            'recipients': [self.user.id],
            'project': self.project.id,
            'task': self.task.id
        }
        response = self.client.post(reverse('notification-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 2)

    def test_get_notification_detail(self):
        response = self.client.get(reverse('notification-detail', kwargs={'pk': self.notification.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.notification.message)

    def test_update_notification(self):
        data = {
            'message': 'Updated notification',
            'recipients': [self.user.id],
            'read': True,
            'project': self.project.id,
            'task': self.task.id
        }
        response = self.client.put(reverse('notification-detail', kwargs={'pk': self.notification.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read)
        self.assertEqual(self.notification.message, 'Updated notification')

    def test_partial_update_notification(self):
        data = {'read': True}
        response = self.client.patch(reverse('notification-detail', kwargs={'pk': self.notification.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read)

    def test_delete_notification(self):
        response = self.client.delete(reverse('notification-detail', kwargs={'pk': self.notification.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Notification.objects.count(), 0)
