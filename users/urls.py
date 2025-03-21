from django.urls import path
from . import views

app_name = 'users'  # This sets the namespace


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    # Fix: Using the correct view name that exists in your views.py
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('otp-login/', views.otp_login_view, name='otp_login'),
    # path('verify-login-otp/', views.verify_login_otp_view, name='verify_login_otp'),
    path('verify-login-otp/', views.verify_otp_view, name='verify_login_otp')


]