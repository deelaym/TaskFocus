from django.urls import path
from . import views


app_name = 'project'

urlpatterns = [
    path('project/', views.ProjectList.as_view(), name='project_list'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<slug:slug>/delete/', views.project_delete, name='project_delete'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('project/<slug:slug>/edit_mode/', views.project_edit_mode, name='project_edit_mode'),
    path('project/<slug:slug>/restart/', views.project_restart, name='project_restart'),
    path('project/<slug:slug>/timer/', views.project_timer, name='project_timer'),
    path('project/<slug:slug>/set_dates/', views.project_set_dates, name='project_set_dates'),
    path('project/<slug:slug>/day/create/', views.day_create, name='day_create'),
    path('project/<slug:slug>/day/<int:day_id>/', views.day_detail, name='day_detail'),
    path('project/<slug:slug>/day/<int:day_id>/complete/', views.day_complete, name='day_complete'),
    path('project/<slug:slug>/day/<int:day_id>/edit/', views.day_edit, name='day_edit'),
    path('project/<slug:slug>/day/<int:day_id>/delete/', views.day_delete, name='day_delete'),
    path('project/<slug:slug>/day/<int:day_id>/create/', views.task_create, name='task_create'),
    path('project/<slug:slug>/day/<int:day_id>/task/<int:task_id>/complete/', views.task_complete, name='task_complete'),
    path('project/<slug:slug>/day/<int:day_id>/task/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('project/<slug:slug>/day/<int:day_id>/task/<int:task_id>/delete/', views.task_delete, name='task_delete'),


]