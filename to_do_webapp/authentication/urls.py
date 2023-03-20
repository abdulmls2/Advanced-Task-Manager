from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views
from authentication.views import  VerificationView

urlpatterns=[

path('Sign_Up', views.Sign_Up, name='Sign_up'),



path('', views.Login, name='Login'),
path('Logout',views.Logout,name='Logout'),
path('login-otp', views.login_otp , name="login_otp"),
path('forget_password', views.forget_password , name="forget_password"),
path('reset_password', views.reset_password , name="reset_password"),
path('update_password', views.update_password , name="update_password"),
path('Sign_Up', views.Sign_Up , name="Sign_Up"),

#url to activate the account
path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),





]