from django.urls import path
from .views import (
    ProjectView, ProjectDetailView,
    TaskView, TaskDetailView,
    FileView, FileDetailView,
    MilestoneView, MilestoneDetailView,
    ProgressReportView, ProgressReportDetailView,
    NotificationView, NotificationDetailView,
    PriorityLevelView, PriorityLevelDetailView,
    FileUploadView, FileListView
)

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('tasks/', TaskView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('files/', FileView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('milestones/', MilestoneView.as_view(), name='milestone-list'),
    path('milestones/<int:pk>/', MilestoneDetailView.as_view(), name='milestone-detail'),
    path('progress-reports/', ProgressReportView.as_view(), name='progress-report-list'),
    path('progress-reports/<int:pk>/', ProgressReportDetailView.as_view(), name='progress-report-detail'),
    path('notifications/', NotificationView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('priority-levels/', PriorityLevelView.as_view(), name='priority-level-list'),
    path('priority-levels/<int:pk>/', PriorityLevelDetailView.as_view(), name='priority-level-detail'),
    path('projects/<int:project_id>/upload/', FileUploadView.as_view(), name='upload_file'),
    path('projects/<int:project_id>/files/', FileListView.as_view(), name='list_files'),
    path('projects/<int:project_id>/files/<int:file_id>/', FileUploadView.as_view(), name='file-detail'),
]
