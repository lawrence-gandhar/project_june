from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from app.models import *
from app.constants import *

import functools

from django.db import connection


#======================================================================
# DECORATOR - TO ALLOW ACCESS ONLY TO ADMINs
#======================================================================
#

def check_url_access(function):

    @functools.wraps(function)
    def inner(request, *args, **kwargs):
        
        profile = user_model.Profile.objects.get(user = request.user)

        if not request.user.is_superuser:
            if profile.usertype == user_constants.IS_USER:
                return redirect("/unautorized/", permanent=False)
        return function(request, *args, **kwargs)
    return inner



#======================================================================
# GET ACCESS RIGHTS OF FOLDER/FILE
#======================================================================
#

def has_access(user_id = None, is_folder = True, ins_id = None):
    
    if user_id is not None :
        
        ret_val = {
            'grant_all' : False,
            'create' : False,
            'rename' : False,
            'delete' : False,
            'upload' : False,
            'move' : False,
            'replace' : False,
        }

        #---------------------------------------------------------------------------------
        # Fetch User instance if user_id is not None
        #---------------------------------------------------------------------------------
        try:
            user = User.objects.get(pk = user_id)
        except:
            return ret_val

        #---------------------------------------------------------------------------------
        # if user is a Super User then grant all permissions are enabled by default
        # return `TRUE`
        if user.is_superuser:
            return dict({
                'grant_all' : True,
                'create' : True,
                'rename' : True,
                'delete' : True,
                'upload' : True,
                'move' : True,
                'replace' : True,
            })

        #---------------------------------------------------------------------------------
        # Fetch User Profile Instance
        #---------------------------------------------------------------------------------
        try:
            user_profile = user_model.Profile.objects.get(user = user)
        except:    
            return ret_val

        #---------------------------------------------------------------------------------
        # If usertype is Admin or Normal User
        #---------------------------------------------------------------------------------
        if user_profile.usertype in [user_constants.IS_ADMIN, user_constants.IS_USER]: 
            
            #---------------------------------------------------------------------------------
            # If a `FOLDER`
            #---------------------------------------------------------------------------------
            if is_folder :
                #---------------------------------------------------------------------------------
                # is not a `Company Folder`
                if ins_id is not None:
                    try:
                        obj = user_model.FolderFilePermissions.objects.get(user = user, folder_id = ins_id)
                    except:
                        return ret_val
                #---------------------------------------------------------------------------------
                # is a `Company Folder`
                # return `TRUE` or `FALSE`
                else:
                    return dict({
                        'grant_all' : user_profile.grant_all,
                        'create' : user_profile.is_create,
                        'rename' : user_profile.is_update,
                        'delete' : user_profile.is_delete,
                        'upload' : user_profile.is_upload,
                        'move' : False,
                        'replace' : False,
                    })

            #---------------------------------------------------------------------------------
            # If a `FILE`
            #---------------------------------------------------------------------------------   
            else:
                try:
                    obj = user_model.FolderFilePermissions.objects.get(user = user, uploaded_file_id = ins_id)
                except:
                    return ret_val

            #---------------------------------------------------------------------------------
            # return `TRUE` or `FALSE` 
            return dict({
                        'grant_all' : obj.perms_grant_all,
                        'create' : obj.perms_create,
                        'rename' : obj.perms_rename,
                        'replace' : obj.perms_replace,
                        'move' : obj.perms_move,
                        'delete': obj.perms_delete,
                        'upload': obj.perms_upload,
                    })

        #---------------------------------------------------------------------------------
        # If usertype is superadmin and grant_all is true
        # return `True`
        elif user_profile.usertype == user_constants.IS_SUPERADMIN and user_profile.grant_all:
            return dict({
                        'grant_all' : user_profile.grant_all,
                        'create' : True,
                        'rename' : True,
                        'delete' : True,
                        'upload' : True,
                        'move' : True,
                        'replace' : True,
                    })

        #---------------------------------------------------------------------------------
        # If all the above fails the return `FALSE`    
        else:
            return ret_val
    return False


#======================================================================
# GET ACCESS RIGHTS OF FOLDER/FILE
#======================================================================
#

def get_folder_permissions(folder_id = None, all_users = True):
    with connection.cursor() as cursor:
        cursor.execute("""select U.username, U.email, U.id as user_id, U.is_superuser, U.first_name, U.last_name,   
            P.grant_all as p_grant_all, P.is_create as p_is_create, P.is_update as p_is_update,  
            P.is_delete as p_is_delete, P.is_upload as p_is_upload, FFP.id as perms_id, FFP.perms_grant_all, 
            FFP.perms_create, FFP.perms_delete, FFP.perms_move, FFP.perms_rename, FFP.perms_replace, 
            FFP.perms_upload, P.usertype 
            from auth_user U, app_folderlist FL
            left join app_profile P on P.user_id = U.id
            left join app_folderfilepermissions FFP on (FFP.folder_id = FL.id and FFP.user_id = U.id 
            and FFP.is_folder = True)
            where is_superuser = False and FL.id = %s""", [folder_id])
        
        q_results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        ret_val = []
        
        for row in q_results:
            ret_val.append(dict(zip(columns, row)))
        
    return ret_val    
        
        
        
        