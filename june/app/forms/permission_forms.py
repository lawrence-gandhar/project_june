#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.contrib.auth.models import User

from django.forms import *
from app.constants import *
from app.models import *


#======================================================================
# FOLDER PERMISSIONS FORM
#======================================================================
#
class FolderPermissionsForm(ModelForm):
    class Meta:
        model = user_model.FolderFilePermissions
        fields = ('user', 'folder', 'perms_grant_all', 'perms_create', 'perms_rename', 
            'perms_move', 'perms_delete', 'perms_upload', 
        )
        
        widgets = {
            'company_name' : TextInput(attrs = {'class':'form-control'}),
            'folder' : TextInput(attrs = {'class':'form-control'}),
            'perms_grant_all' : Select(attrs = {'class':'form-control'}, choices=user_constants.IS_ACTIVE),
            'perms_create' : Select(attrs = {'class':'form-control'}, choices=user_constants.IS_ACTIVE),
            'perms_rename' : Select(attrs = {'class':'form-control'}, choices=user_constants.IS_ACTIVE),
            'perms_move' : Select(attrs = {'class':'form-control'}, choices=user_constants.IS_ACTIVE),
            'perms_delete' : Select(attrs = {'class':'form-control'}, choices=user_constants.IS_ACTIVE),
            'perms_upload' : Select(attrs = {'class':'form-control'}, choices=user_constants.IS_ACTIVE),
        }
        


