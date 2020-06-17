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
from . import folder_management

import os, shutil
import pandas as pd
import numpy as np

from datetime import datetime


#======================================================================
# Dashboard View
#======================================================================
#

class DashboardView(View):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/dashboard/dashboard.html'

    data["css_files"] = []
    data["js_files"] = []

    data["page_title"] = "Dashboard"
    
    #
    #
    def get(self, request):
        
        self.data["users_count"] = User.objects.filter(is_superuser = False).count()
        self.data["companies"] = user_model.Company.objects.all().count()
        self.data["folders"] = user_model.FolderList.objects.all().count()
        self.data["files"] = user_model.UploadedFiles.objects.all().count()
    
    
        return render(request, self.template_name, self.data)
    
