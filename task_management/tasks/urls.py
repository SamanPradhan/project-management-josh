from django.urls import path
from .views import user_list, user_detail, task_list, task_detail, tasks_assigned_to_user, assign_assignees_to_task

urlpatterns = [
    # User CRUD endpoints
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),

    # Task CRUD endpoints
    path('tasks/', task_list, name='task-list'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),

    # Custom endpoint to get tasks for a specific user
    path('tasks/assigned-to/<int:user_id>/', tasks_assigned_to_user, name='tasks-assigned-to'),
    path('tasks/<int:pk>/assign-to/', assign_assignees_to_task)
]

