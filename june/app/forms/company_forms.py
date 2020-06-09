#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import *
from app.constants import *
from app.models import *

#
#
#
class CompanyForm(ModelForm):
    class Meta:
        model = user_model.Company
        fields = ('company_name', 'description', 'folder_name')
        
        widgets = {
            'company_name' : TextInput(attrs = {'class':'form-control'}),
            'folder_name' : TextInput(attrs = {'class':'form-control'}),
            'description' : Textarea(attrs = {'class':'form-control'}),
        }
   
#
#
#
class FolderForm(ModelForm):
    class Meta:
        model = user_model.FolderList
        fields = ('folder_name',)
        
        widgets = {
            'folder_name' : TextInput(attrs = {'class':'form-control'}),
        }
        
        
#
#
#
class UploadFileForm(ModelForm):
    class Meta:
        model = user_model.UploadedFiles
        fields = ('uploaded_file',)
        
        widgets = {
            'uploaded_file' : FileInput(attrs = {'class':'form-control', 'onchange':'checkfile(this)', 'required':'true'}),
        }        