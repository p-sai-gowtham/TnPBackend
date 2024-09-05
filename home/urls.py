from . import views
from django.urls import path,include
from django.conf import settings

app_name= 'app'

urlpatterns = [
    path("student", views.all_students,name="student"), # type: ignore
    path("student/<str:pk>", views.student),
    path('job_applications', views.add_job_applications, name='create_job_application'),
    path('delete_job_application/<int:pk>', views.delete_job_application, name='delete_job_application'),
    path('edit_job_application/<int:pk>', views.edit_job_application, name='edit_job_application'),
    path('get_job_application/<int:pk>', views.job_application, name='get_job_application'),
    path('add_drive_data',views.add_drive_data, name="add_drive_data"),
    path("upload/<str:type>",views.upload_resume, name="upload_resume"),
    path('get_all_job_applications', views.get_all_job_applications, name='get_all_job_applications'),
    path('submit_application', views.submit_application, name='submit_application'),
    path('get_applied_applications', views.get_applied_applications, name='get_applied_applications'),
    path('get_applied_students', views.get_applied_students, name='get_applied_students'),
    path('job_company_name', views.job_company_name, name='job_company_name'),
]

