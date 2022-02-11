from django.urls import path 
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('update-todo/<int:pk>', views.update_todo, name='update-todo'),
    path('delete-todo/<int:pk>', views.delete_todo, name='delete-todo'),
    path('delete-task/<int:pk>', views.DeleteTask.as_view(), name='delete-task'),
    path('tasklist/', views.AllTask.as_view(), name='task-list'),
    path('view-task/<int:pk>', views.task_detail, name='task-detail'),
    path('update-task/<int:pk>', views.update_task, name='task-update'),
    path('new-task/', views.create_task, name='new-task'),
    path('whats-this-day/', views.on_day, name="whats-this-day"),
]

