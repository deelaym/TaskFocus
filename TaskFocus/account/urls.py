from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('<slug:username>/settings/', views.account_settings, name='account_settings'),
    path('<slug:username>/delete/', views.account_delete, name='account_delete'),
]
