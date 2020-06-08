#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from collections import defaultdict

from django.conf import settings

from app.models import *
from app.forms import *
from . import folder_management

import os, shutil
import pandas as pd


#======================================================================
# Handle File
#======================================================================
#


def handle_uploaded_file(f, company, parent_folder):

    folder_path = None
    company_path = os.path.join(settings.COMPANY_FOLDER_PATH,company.folder_name)
    
    if parent_folder is None:
        folder_path = company_path
    else:              
        folder_path = folder_management.folder_parents(parent_folder.id, [], company_path)
    
    if folder_path is not None:
        dest = os.path.join(folder_path,f.name);
        with open(dest, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

#======================================================================
# Get File Path
#======================================================================
#

def get_file_path(ins = None):
    if ins is not None:
        company_path = os.path.join(settings.COMPANY_FOLDER_PATH,ins.company.folder_name)

        if ins.company_folder:
            return company_path
        else:
            if ins.folder_path is not None:
                folder_path = folder_management.folder_parents(ins.folder_path.id, [], company_path)
                return folder_path
            return False
    return False


#======================================================================
# Upload File
#======================================================================
#

def upload_file(request):
    if request.method == 'POST':
        form = company_forms.UploadFileForm(request.POST, request.FILES)
        company = request.POST["company_ids"] if request.POST["company_ids"] !="" else None
        parent_folder = request.POST["parent_folder_ids"] if request.POST["parent_folder_ids"] !="" else None
                
        try:
            comp_ins = user_model.Company.objects.get(pk = int(company))
        except:
            return False
        
        if parent_folder is not None:
            try:
                parent = user_model.FolderList.objects.get(pk = int(parent_folder))
            except:
                return redirect("/unauthorized/", permanent=False)
        else:
            parent = None
         
        if form.is_valid():
            if company is not None:   
                handle_uploaded_file(request.FILES['uploaded_file'], comp_ins, parent)  
                
                ins = form.save(commit = False) 
    
                if parent is None:
                    ins.company_folder = True
                else:
                    ins.folder_path = parent
                    ins.company_folder = False
                    
                ins.company = comp_ins
                ins.user = request.user
                ins.save()
            else:
                return redirect("/unauthorized/",permanent=False)
                
        if parent_folder is None:  
            return redirect('/manage_folder/'+str(company)+"/",permanent=False)
        else:
            return redirect('/manage_folder/'+str(company)+"/"+str(parent_folder)+"/", permanent=False)
    return redirect("/unauthorized/",permanent=False)

#
#
#
#
class FileView(View):

    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/file_management/file_view.html'

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/file_management.js']

    data["page_title"] = "Manage File"

    #
    #
    #
    def get(self, request, ins=None):
        try:
            file_ins = user_model.UploadedFiles.objects.get(pk = int(ins))  
        except:
            return redirect("/unauthorized/", permanent=False)

        fd = os.path.join(get_file_path(file_ins),file_ins.uploaded_file)

        df = pd.read_excel(fd, header=0)  
        self.data["data_html"] = df.to_html()
        return render(request, self.template_name, self.data)

