from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task, File, Notification, PriorityLevel, ProjectFile, Status
from .serializers import ProjectSerializer, TaskSerializer, FileSerializer, NotificationSerializer, PriorityLevelSerializer, ProjectFileSerializer, StatusSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
import os

class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        project_id = request.query_params.get('project')
        if project_id:
            queryset = Task.objects.filter(project=project_id)
        else:
            queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = File.objects.all()
        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Notification.objects.all()
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        notification = self.get_object(pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        notification = self.get_object(pk)
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):  # Adding PATCH method
        notification = self.get_object(pk)
        serializer = NotificationSerializer(notification, data=request.data, partial=True)  # Specify partial=True for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        notification = self.get_object(pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PriorityLevelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = PriorityLevel.objects.all()
        serializer = PriorityLevelSerializer(queryset, many=True)
        return Response(serializer.data)

class PriorityLevelDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return PriorityLevel.objects.get(pk=pk)
        except PriorityLevel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        priority_level = self.get_object(pk)
        serializer = PriorityLevelSerializer(priority_level)
        return Response(serializer.data)
    
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, file_id):
        try:
            project_file = ProjectFile.objects.get(id=file_id, project_id=project_id)
            serializer = ProjectFileSerializer(project_file)
            return Response(serializer.data)
        except ProjectFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, project_id):
        files = request.FILES.getlist('file')
        for file in files:
            data = {'file': file, 'project': project_id, 'uploaded_by': request.user.id}
            serializer = ProjectFileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Files uploaded successfully!"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, project_id, file_id):
        try:
            project_file = ProjectFile.objects.get(id=file_id, project_id=project_id)
        except ProjectFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        file_path = os.path.join("media", str(project_file.file))
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete the database entry
        project_file.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class FileListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        project_files = ProjectFile.objects.filter(project_id=project_id)
        serializer = ProjectFileSerializer(project_files, many=True)
        return Response(serializer.data)
    

class StatusListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Status.objects.all()
        serializer = StatusSerializer(queryset, many=True)
        return Response(serializer.data)

class StatusDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Status.objects.get(pk=pk)
        except Status.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        status_instance = self.get_object(pk)
        serializer = StatusSerializer(status_instance)
        return Response(serializer.data)
