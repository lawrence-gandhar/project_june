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
        
        xc = permissions_helper.get_folder_permissions(folder_id = ins, all_users = True)
        
        self.data["users_permissions_list"] = xc 
    
        return render(request, self.template_name, self.data)
    
    
    
    
    