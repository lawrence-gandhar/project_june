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
# Get Folder Path
#======================================================================
#

def folder_parents(parent_id, parents_ids=[], main_folder=None):
    
    if main_folder is not None:
        if parent_id is None :
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
                    parent_id = folderlist.parent_folder.id
            except:
                run = False

        parents_folders.reverse()
           
        old_path = os.path.join(settings.COMPANY_FOLDER_PATH, main_folder)
        path = os.path.join(old_path, os.path.join(*parents_folders))
                
        return path
    return False
    

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
    
    #---------------------------------------------------------------------------------
    # GET REQUEST
    #---------------------------------------------------------------------------------
    #
    def get(self, request, company=None, parent_folder=None):

        self.data["company_ids"] = company        
        self.data["parent_folder_ids"] = parent_folder if parent_folder is not None else ""

        #---------------------------------------------------------------------------------
        # FETCH COMPANY INSTANCE
        #--------------------------------------------------------------------------------- 
        #
        try:
            comp = user_model.Company.objects.get(pk = int(company))
        except:
            return redirect("/unauthorized/", permanent=False)
        
        #---------------------------------------------------------------------------------
        # Permissions
        #--------------------------------------------------------------------------------- 
        #
        self.data["has_access"] = permissions_helper.has_access(user_id = request.user.id, is_folder = True, ins_id = parent_folder)
        
        print(self.data["has_access"])

        #---------------------------------------------------------------------------------
        # FILE UPLOADING FORM & FOLDER CREATION FORM
        #---------------------------------------------------------------------------------
        #
        self.data["upload_file_form"] = company_forms.UploadFileForm()
        self.data["add_folder_form"] = company_forms.FolderForm() 

        #---------------------------------------------------------------------------------
        # Get the list of folders in the current folder
        #---------------------------------------------------------------------------------
        #
        folderlist = user_model.FolderList.objects.filter(company = comp)
        if parent_folder is not None:
            folderlist = folderlist.filter(parent_folder_id = int(parent_folder))        

            try:
                parent = user_model.FolderList.objects.get(pk = int(parent_folder))
            except:
                return redirect("/unauthorized/", permanent=False)
        
            self.data["folder_path"] = folder_parents(parent_folder, [], comp.folder_name)   

        else:
            folderlist = folderlist.filter(parent_folder__isnull = True)
            self.data["folder_path"] = os.path.join(settings.COMPANY_FOLDER_PATH, comp.folder_name)
         
        self.data["folder_list"] = folderlist
        
        #---------------------------------------------------------------------------------
        # get the list of files in the current folder
        #---------------------------------------------------------------------------------
        #
        filelist = user_model.UploadedFiles.objects.filter(company = comp)
        if parent_folder is not None:
            filelist = filelist.filter(folder_path_id = int(parent_folder))
        else:
            filelist = filelist.filter(company_folder = True, folder_path__isnull = True)
         
        self.data["filelist"] = filelist
        
        #---------------------------------------------------------------------------------
        # Create Rename Folder Forms
        #--------------------------------------------------------------------------------- 
        #  
        self.data["rename_folder_form"] = []
        i = 0
        for folder in folderlist:
            xx = {}
            xx["company_ids"] = folder.company.id
            xx["parent_folder_ids"] = folder.parent_folder.id if folder.parent_folder is not None else ""
            xx["form_prefix"] = "form_"+str(i)
            xx["ids"] = folder.id
            xx["form"] = company_forms.FolderForm(instance=folder, prefix="form_"+str(i))
            self.data["rename_folder_form"].append(xx)
            
            i +=1

        return render(request, self.template_name, self.data)

    #---------------------------------------------------------------------------------
    # POST REQUEST
    #---------------------------------------------------------------------------------
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

        if folderlist.parent_folder is not None:        
            fd = folder_parents(folderlist.parent_folder.id, [], folderlist.company.folder_name) 
            path = os.path.join(fd, folderlist.folder_name)
        else:
            path = os.path.join(settings.COMPANY_FOLDER_PATH, folderlist.company.folder_name, folderlist.folder_name)
        
        folderlist.delete()
        
        try:
            shutil.rmtree(path)
        except:
            pass
        return HttpResponse(1)
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
        
        fd = os.path.join(settings.COMPANY_FOLDER_PATH, folder.company.folder_name)
        
        if parent_id !="":
            fd = folder_parents(folder.parent_folder.id, [], folder.company.folder_name) 
        
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
    
        