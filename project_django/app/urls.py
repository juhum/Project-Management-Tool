from django.urls import path
from .views import (
    ProjectView, ProjectDetailView,
    TaskView, TaskDetailView,
    FileView, FileDetailView,
    NotificationView, NotificationDetailView,
    PriorityLevelView, PriorityLevelDetailView,
    FileUploadView, FileListView,
    StatusListView, StatusDetailView,
)
urlpatterns = [
    path('projects/', ProjectView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('tasks/', TaskView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('notifications/', NotificationView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('priority-levels/', PriorityLevelView.as_view(), name='priority-level-list'),
    path('priority-levels/<int:pk>/', PriorityLevelDetailView.as_view(), name='priority-level-detail'),
    path('projects/<int:project_id>/upload/', FileUploadView.as_view(), name='upload_file'),
    path('projects/<int:project_id>/files/', FileListView.as_view(), name='list_files'),
    path('projects/<int:project_id>/files/<int:file_id>/', FileUploadView.as_view(), name='file-detail'),
    path('statuses/', StatusListView.as_view(), name='status-list'),
    path('statuses/<int:pk>/', StatusDetailView.as_view(), name='status-detail'),
]
