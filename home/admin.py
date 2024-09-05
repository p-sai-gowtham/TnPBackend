from django.contrib import admin
from .models import Document, JobApplication, AppliedApplication


# Register your models here.
admin.site.register(Document)

admin.site.register(JobApplication) 
admin.site.register(AppliedApplication)