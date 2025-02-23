from django.urls import path
from . import views

urlpatterns = [

    path('verify-user/', views.verify_user, name='verify_user'),
    path('user-info/', views.get_user_info, name='user_info'),
    
    # Tasks
    path('tasks/', views.get_active_tasks, name='active_tasks'),
    path('submit-progress/', views.submit_progress, name='submit_progress'),
    path('task-progress/<int:task_id>/', views.get_task_progress, name='task_progress'),
    
    # Admin 
    path('mark-progress/<int:progress_id>/', views.mark_progress, name='mark_progress'),
    path('export-users/', views.export_users, name='export_users'),
    
]