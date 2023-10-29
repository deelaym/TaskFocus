from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('project/<slug:slug>/day/create/', views.day_form, name='day_create'),
]