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

import os, shutil



#======================================================================
# Get Folder Path
#======================================================================
#

def folder_parents(parent_id, parents_ids=[], main_folder=None):
    
    if parent_id is None:
        return os.path.join(settings.COMPANY_FOLDER_PATH, main_folder)
    
    parents_folders = parents_ids
    run = True
    
    while run:

        try:
            folderlist = user_model.FolderList.objects.get(pk = int(parent_id))
            
            if folderlist.parent_folder is None:
                parents_folders.append(folderlist.folder_name) 
                run = False
            else:
                parents_folders.append(folderlist.folder_name) 
                parent_id = folderlist.parent_folder
        except:
            run = False

    parents_folders.reverse()
       
    old_path = os.path.join(settings.COMPANY_FOLDER_PATH, main_folder)
    path = os.path.join(old_path, os.path.join(*parents_folders))
            
    return path
    

#======================================================================
# Manage Company View
#======================================================================
#

class ManageFolderView(View):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/folder_management/manage_folder.html'

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/folder_management.js']

    data["page_title"] = "Manage Folder"
        
    #
    #
    def get(self, request, company=None, parent_folder=None):
        try:
            comp = user_model.Company.objects.get(pk = int(company))
        except:
            return redirect("/unauthorized/", permanent=False)
        
        self.data["company_ids"] = company
        
        self.data["parent_folder_ids"] = parent_folder if parent_folder is not None else ""
        
        self.data["add_folder_form"] = company_forms.FolderForm() 

        #
        #
        folderlist = user_model.FolderList.objects.filter(company = comp)
        if parent_folder is not None:
            folderlist = folderlist.filter(parent_folder_id = int(parent_folder))
        else:
            folderlist = folderlist.filter(parent_folder__isnull = True)
         
        self.data["folder_list"] = folderlist
        
        #
        #
        self.data["rename_folder_form"] = []
        i = 0
        for folder in folderlist:
            xx = {}
            xx["company_ids"] = folder.company.id
            xx["parent_folder_ids"] = folder.parent_folder if folder.parent_folder is not None else ""
            xx["form_prefix"] = "form_"+str(i)
            xx["ids"] = folder.id
            xx["form"] = company_forms.FolderForm(instance=folder, prefix="form_"+str(i))
            self.data["rename_folder_form"].append(xx)
            
            i +=1
                       
        return render(request, self.template_name, self.data)

    #
    #
    def post(self, request, company=None, parent_folder=None):
    
        try:
            comp = user_model.Company.objects.get(pk = int(company))
        except:
            return redirect("/unauthorized/", permanent=False)
            
        #
        form = company_forms.FolderForm(request.POST)         
        new_folder = form.data["folder_name"]
        
        if parent_folder is not None:        
            
            try:
                parent = user_model.FolderList.objects.get(pk = int(parent_folder))
            except:
                return redirect("/unauthorized/", permanent=False)
        
            fd = folder_parents(parent_folder, [], comp.folder_name)              
            
            new_path = os.path.join(fd,new_folder)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                
            ins = form.save(commit=False)    
            ins.company = comp
            ins.parent_folder = parent
            ins.save()
        else:            
            new_path = os.path.join(settings.COMPANY_FOLDER_PATH, comp.folder_name, new_folder)
            
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            
            ins = form.save(commit=False)    
            ins.company = comp
            ins.save()
          
        if parent_folder is None: 
            return redirect("/manage_folder/"+str(company), permanent=False)
        else:
            return redirect("/manage_folder/"+str(company)+"/"+str(parent_folder)+"/", permanent=False)
        

#======================================================================
# Delete Folder
#======================================================================
#
def delete_folder(request, ins=None):
    if ins is not None:
        
        folderlist = user_model.FolderList.objects.get(pk = int(ins))        
        fd = folder_parents(folderlist.parent_folder, [], folderlist.company.folder_name)   
        path = os.path.join(fd, folderlist.folder_name)
        
        try:
            shutil.rmtree(path)
            folderlist.delete()
            return HttpResponse(1)
        except:
            return HttpResponse(0)
    return HttpResponse(0)


#======================================================================
# Rename Folder
#======================================================================
#
def rename_folder(request):
    if request.POST:
        form_prefix = request.POST["form_prefix"]
        company_id = request.POST["company_ids"]
        parent_id = request.POST["parent_folder_ids"]
        ins = request.POST["ins"]
        
        folder = user_model.FolderList.objects.get(pk = int(ins))
        fd = folder_parents(folder.parent_folder, [], folder.company.folder_name)     
        old_path = os.path.join(fd, folder.folder_name)
        
        form = company_forms.FolderForm(request.POST,instance=folder, prefix=form_prefix)
        
        if form.is_valid():
        
            new_path = os.path.join(fd,form.data[form_prefix+"-folder_name"])
            
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                form.save()
        
        if parent_id =="": 
            return redirect("/manage_folder/"+str(company_id)+"/", permanent=False)
        else:
            return redirect("/manage_folder/"+str(company_id)+"/"+str(parent_id)+"/", permanent=False)
    return redirect("/unauthorized/", permanent=False)    

        