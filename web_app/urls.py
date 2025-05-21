from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('security_question/', views.security_question, name='security_question'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_user/', views.delete_user, name='delete_user'),
]