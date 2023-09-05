"""
URL configuration for JobGPTFilterServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from data_management_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('write-to-db/', views.write_to_db, name='write_to_db'),
    path('show-filtered-jobs/', views.show_jobs, name='show_jobs'),
    path('show-filtered-jobs/start-gpt-filtering/', views.start_gpt_filtering, name='start_gpt_filtering'),
    path('show-filtered-jobs/reset-all-status/', views.reset_all_status, name='reset_all_status')
]
