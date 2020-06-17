from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from app.models import *
from app.constants import *

#======================================================================
# FULL PERMISSION ON A FOLDER/FILE
#======================================================================
#

def user_full_access(user_id = None, is_folder = True, ins_id = None):
    
    if user_id is not None :
        
        #
        # Fetch User instance if user_id is not None
        #
        try:
            user = User.objects.get(pk = user_id)
        except:
            return False

        #
        # Fetch User Profile Instance
        #
        try:
            user_profile = user_model.Profile.objects.get(user = user)
        except:    
            return False

        #
        # If usertype is Admin or Normal User
        #
        if user_profile.usertype in [user_constants.IS_ADMIN, user_constants.IS_USER]: 
            
            #
            # If a `FOLDER`
            #
            if is_folder :
                #
                # is not a `Company Folder`
                #
                if ins_id is not None:
                    try:
                        obj = user_model.FolderFilePermissions.objects.get(user = user, folder_id = ins_id)
                    except:
                        return False
                #
                # is a `Company Folder`
                # return `TRUE` or `FALSE`
                else:
                    return user_profile.grant_all

            #
            # If a `FILE`
            #         
            else:
                try:
                    obj = user_model.FolderFilePermissions.objects.get(user = user, uploaded_file_id = ins_id)
                except:
                    return False

            #
            # return `TRUE` or `FALSE` 
            return obj.perms_grant_all

        #
        # If usertype is superadmin and grant_all is true
        # return `True`
        elif user_profile.usertype == user_constants.IS_SUPERADMIN and user_profile.grant_all:
            return True

        #
        # if user is a Super User then grant all permissions are enabled by default
        # return `TRUE`
        elif user.is_superuser:
            return True

        #
        # If all the above fails the return `FALSE`    
        else:
            return False
    return False

#======================================================================
# CREATE PERMISSION ON A FOLDER/FILE
#======================================================================
#
