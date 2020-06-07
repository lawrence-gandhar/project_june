from django.contrib import admin
from app.models import *

# Register your models here.

#
#
@admin.register(user_model.Profile)
class Profile(admin.ModelAdmin):
    model = user_model.Profile

#
#
@admin.register(user_model.Company)
class Company(admin.ModelAdmin):
    model = user_model.Company


#
#
@admin.register(user_model.UploadedFiles)
class UploadedFiles(admin.ModelAdmin):
    model = user_model.UploadedFiles
