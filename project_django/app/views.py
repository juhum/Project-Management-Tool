from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task, File, Milestone, ProgressReport, Notification, PriorityLevel, ProjectFile
from .serializers import ProjectSerializer, TaskSerializer, FileSerializer, MilestoneSerializer, ProgressReportSerializer, NotificationSerializer, PriorityLevelSerializer, ProjectFileSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

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
            return Response(status=status.HTTP_404_NOT_FOUND)

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
    

class MilestoneView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Milestone.objects.all()
        serializer = MilestoneSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MilestoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MilestoneDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Milestone.objects.get(pk=pk)
        except Milestone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        milestone = self.get_object(pk)
        serializer = MilestoneSerializer(milestone)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        milestone = self.get_object(pk)
        serializer = MilestoneSerializer(milestone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        milestone = self.get_object(pk)
        milestone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProgressReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = ProgressReport.objects.all()
        serializer = ProgressReportSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProgressReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProgressReportDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProgressReport.objects.get(pk=pk)
        except ProgressReport.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        progress_report = self.get_object(pk)
        serializer = ProgressReportSerializer(progress_report)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        progress_report = self.get_object(pk)
        serializer = ProgressReportSerializer(progress_report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        progress_report = self.get_object(pk)
        progress_report.delete()
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

    def post(self, request, format=None):
        serializer = PriorityLevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def put(self, request, pk, format=None):
        priority_level = self.get_object(pk)
        serializer = PriorityLevelSerializer(priority_level, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        priority_level = self.get_object(pk)
        priority_level.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class FileUploadView(APIView):

    def get(self, request, project_id, file_id):
        try:
            project_file = ProjectFile.objects.get(id=file_id, project_id=project_id)
            serializer = ProjectFileSerializer(project_file)
            return Response(serializer.data)
        except ProjectFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, project_id, file_id):
        try:
            project_file = ProjectFile.objects.get(id=file_id, project_id=project_id)
        except ProjectFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        project_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class FileListView(APIView):
    def get(self, request, project_id):
        project_files = ProjectFile.objects.filter(project_id=project_id)
        serializer = ProjectFileSerializer(project_files, many=True)
        return Response(serializer.data)
    
