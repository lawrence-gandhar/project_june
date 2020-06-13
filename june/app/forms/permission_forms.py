#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.contrib.auth.models import User

from django.forms import *
from app.constants import *
from app.models import *

#
#
#
class FolderPermissionsForm(ModelForm):
    class Meta:
        model = user_model.FolderPermissions
        fields = ('user', 'folder', 'permissions')
        
        widgets = {
            'company_name' : TextInput(attrs = {'class':'form-control'}),
            'folder_name' : TextInput(attrs = {'class':'form-control'}),
            'permissions' : Select(attrs = {'class':'form-control'}),
        }