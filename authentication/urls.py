from django.contrib import admin
from django.urls import include, path

from authentication import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('jobseekerhome/', views.jobseekerhome, name='jobseekerhome'),
   
]