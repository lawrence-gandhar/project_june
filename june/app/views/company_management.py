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
# Manage Company View
#======================================================================
#
class ManageCompanyView(View):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/company_management/manage_company.html'

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/company_form.js']

    data["page_title"] = "Manage Company"
    
    data["redirecter"] = "/manage_company/"
    data["is_ajax"] = False
    
    #
    #
    
    def get(self, request):
        
        self.data["company_list"] = user_model.Company.objects.all().order_by("-id")  
        self.data["company_form"] = company_forms.CompanyForm()        
        
        self.data["edit_company_forms"] = []
        i = 0
        
        for company in self.data["company_list"]:  
            xx = {}
            xx["ids"] = company.id
            xx["form_prefix"] = "form_"+str(i)
            xx["folder_present"] = True if company.folder_name is not None else False
            xx["form"] = company_forms.CompanyForm(instance=company, prefix="form_"+str(i))
            self.data["edit_company_forms"].append(xx)
            
            i +=1
                                    
        return render(request, self.template_name, self.data)
        
        
        
#======================================================================
# Add Company View
#======================================================================
#

def add_company(request):
    company = company_forms.CompanyForm(request.POST)
    
    if company.is_valid():
        ins = company.save(commit = False)
        ins.user = request.user
        ins.is_active = True        
        
        folder_name = company.data["folder_name"]
        
        if folder_name !="":
            new_path = os.path.join(settings.COMPANY_FOLDER_PATH,folder_name)
            
            if not os.path.exists(new_path):
                try:
                    os.makedirs(new_path)
                except:
                    ret_val = 0
            else:
                ret_val = 0
        
        ins.save()
        
        ret_val = 1
    else:
        ret_val = 0
    
    if request.POST["is_ajax"] == "True":
        return HttpResponse(ret_val)
    else:    
        return redirect(request.POST["redirecter"],permanent=False)


#======================================================================
# Add Company View
#======================================================================
#

def edit_company(request):
    if request.POST:
        
        form_prefix = request.POST["form_prefix"]
        
        try:
            comp = user_model.Company.objects.get(pk = int(request.POST["ids"]))
        except:
            return redirect("/unauthorized/", permanent=False)   

        company = company_forms.CompanyForm(request.POST, instance=comp, prefix=form_prefix)
        
        if comp.folder_name is not None:        
            old_path = os.path.join(settings.COMPANY_FOLDER_PATH,comp.folder_name)
        
        #
        #
        if company.is_valid():  
    
            new_folder = company.data[form_prefix+"-folder_name"]
            
            if new_folder != "":            
                new_path = os.path.join(settings.COMPANY_FOLDER_PATH,new_folder)
                
                #
                #
                if request.POST["folder_rename"] == "0":     
                    # Rename Folder
                    if not os.path.exists(new_path):     
                        if not os.path.exists(old_path):
                            os.makedirs(new_path)
                        else:
                            os.rename(old_path, new_path)                
                else:
                    # Create New Folder                          
                    if not os.path.exists(new_path):                    
                        os.makedirs(new_path)
            company.save()
                    
        return redirect("/manage_company/",permanent=False)
    return redirect("/unauthorized/", permanent=False)   
                
#======================================================================
# Delete Company View
#======================================================================
#

def delete_company(request, ins=None):

    if request.is_ajax() and ins is not None:      
        try:
            company = user_model.Company.objects.get(pk = int(ins))  
            
            if company.folder_name:
                try:
                    folder_path = os.path.join(settings.COMPANY_FOLDER_PATH,company.folder_name)
                    shutil.rmtree(folder_path)
                except:
                    return HttpResponse(0)   
            company.delete()            
            return HttpResponse(1)
        except:
            return HttpResponse(0)
    return HttpResponse(0)
    
        
#======================================================================
# Delete Company Folder
#======================================================================
#        

def delete_company_folder(request, ins = None):
    if request.is_ajax() and ins is not None:
        try:
            company = user_model.Company.objects.get(pk = int(ins))            
            try:
                folder_path = os.path.join(settings.COMPANY_FOLDER_PATH,company.folder_name)
            except:
                return HttpResponse(1)
                
            try:
                shutil.rmtree(folder_path)
                
                company.folder_name = None
                company.save()
                
                return HttpResponse(1)
            except:
                return HttpResponse(0)            
        except:
            return HttpResponse(0)
    return HttpResponse(0)
 
 
#======================================================================
# Delete Company Folder
#======================================================================
#  

def change_company_status(request, ins = None, status = 1):    
    if ins is not None:
        try:
            company = user_model.Company.objects.get(pk = int(ins))  
            company.is_active = status
            company.save()
            
            return redirect("/manage_company/",permanent=False)
        except:
            return redirect("/unauthorized/", permanent=False)  
    return redirect("/unauthorized/", permanent=False)  


#======================================================================
# Manage Company View
#======================================================================
#

def EmpCompanyView(request):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/company_management/employee_company_view.html'

    data["css_files"] = []
    data["js_files"] = []

    data["page_title"] = "View Company"
    
    data["company_list"] = user_model.Company.objects.all().order_by("-id")  
        
    return render(request, template_name, data)

    
    
    