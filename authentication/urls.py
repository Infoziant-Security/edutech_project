from django.contrib import admin
from django.urls import include, path

from authentication import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('jobseekerhome/', views.jobseekerhome, name='jobseekerhome'),
    path('candidate_profile/', views.candidate_profile, name='candidate_profile'),
    path('create-job-opening/', views.create_job_opening, name='create_job_opening'),
    path('view-job-openings/', views.view_job_openings, name='view_job_openings'),
    path('employerhome/', views.employer_home, name='employer_home'),
    path('candidate-view-jobs/', views.candidate_view_jobs, name='candidate_view_jobs'),
    path('job-detail/<int:job_id>/', views.job_detail, name='job_detail'),
    path('dashboard-manage-job/', views.dashboard_manage_job, name='dashboard_manage_job'),
    path('about/', views.about, name='about'),
    path('jobs/', views.jobs, name='jobs'),
    path('companies/', views.companies, name='companies'),
    path('courses/', views.courses, name='courses')
]