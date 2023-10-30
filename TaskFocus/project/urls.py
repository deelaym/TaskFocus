from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('project/<slug:slug>/day/create/', views.day_create, name='day_create'),
    path('project/<slug:slug>/day/<int:id>/create/', views.task_create, name='task_create'),
    path('project/<slug:slug>/day/<int:day_id>/task/<int:task_id>/', views.task_complete, name='task_complete'),

]