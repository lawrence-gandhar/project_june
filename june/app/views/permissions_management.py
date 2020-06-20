#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

from collections import defaultdict

from django.conf import settings

from app.models import *
from app.forms import *
from app.helpers import *

import os, shutil


#======================================================================
# FOLDER/FILE PERMISSIONS
#======================================================================
#

class ManageFolderPermissions(View):
    
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/permissions_config_management/manage_permissions.html'

    data["css_files"] = []
    data["js_files"] = []

    data["page_title"] = "Manage Folder Permissions"
    
    #
    #
    #
    def get(self, request, company=None, parent_folder=None, ins=None):
        try:
            folder = user_model.FolderList.objects.get(pk = int(ins))
        except:
            return redirect("/unauthorized/", permanent=False)
        
        self.data["users_permissions_list"] = permissions_helper.get_folder_permissions(folder_id = ins, all_users = True) 
        
        self.data["form"] = configuration_forms.FolderPermissionsForm()        
    
        return render(request, self.template_name, self.data)
    
    #
    #
    #
    def post(self, request, company=None, parent_folder=None, ins=None):
            
        try:
            folder = user_model.FolderList.objects.get(pk = int(ins))
        except:
            return redirect("/unauthorized/", permanent=False)

        try:
            f_ins = user_model.FolderFilePermissions.objects.get(user=request.user, is_folder=True, folder = folder)
            form = configuration_forms.FolderPermissionsForm(request.POST, instance=f_ins)
        except:
            form = configuration_forms.FolderPermissionsForm(request.POST)
            
        if form.is_valid():
            form_ins = form.save(commit=False)
            form_ins.folder = folder
            
            
        
    
    
    