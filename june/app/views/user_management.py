#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

from collections import defaultdict

from app.models import *
from app.forms import *



#======================================================================
# AddUser View
#======================================================================
#

class AddUserView(View):
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/user_management/add_users.html'

    data["css_files"] = []
    data["js_files"] = [                
                'base_files/assets/libs/inputmask/dist/min/jquery.inputmask.bundle.min.js',
                'base_files/dist/js/pages/mask/mask.init.js',
                'custom_files/js/common.js',
                'custom_files/js/user_form.js',
            ]

    data["page_title"] = "Add User"
    data["errors"] = []    
    data["edit_mode"] = False
    
    
    #
    #
    def get(self, request):    
        self.data["user_creation_form"] = user_forms.CreateUserForm()        
        self.data["profile_form"] = user_forms.ProfileForm()
        return render(request, self.template_name, self.data)
        
    #
    #
    def post(self, request):
        user_form = user_forms.CreateUserForm(request.POST)

        if user_form.is_valid():
            ins = user_form.save()
            
            try:
                profile = user_model.Profile.objects.get(user = ins)
                
                grant_all = request.POST.get("grant_all", False)
                is_create = request.POST.get("is_create", False)
                is_update = request.POST.get("is_update", False)
                is_delete = request.POST.get("is_delete", False)
                is_upload = request.POST.get("is_upload", False)
                
                profile.grant_all = grant_all
                profile.is_create = is_create
                profile.is_update = is_update
                profile.is_delete = is_delete
                profile.is_upload = is_upload
                profile.usertype = request.POST["usertype"]
                    
                profile.save()    
            except:
                User.objects.get(instance = user).delete()
                self.data["errors"] = ["Error Occurred. User Creation Failed"]
                
            self.data["errors"] = []
        else:
            self.data["errors"] = user_form.errors

        return redirect("/add_user/",permanent=False)
  
#======================================================================
# EditUser View
#======================================================================
#

class EditUserView(View):
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/user_management/add_users.html'

    data["css_files"] = []
    data["js_files"] = [                
                'base_files/assets/libs/inputmask/dist/min/jquery.inputmask.bundle.min.js',
                'base_files/dist/js/pages/mask/mask.init.js',
                'custom_files/js/common.js',
                'custom_files/js/user_form.js',
            ]

    data["page_title"] = "Edit User"
    data["errors"] = []
    data["edit_mode"] = True
    
    #
    #
    def get(self, request, ins = None):  
        try:
            user = User.objects.get(pk = int(ins))
        except:
            return redirect("/unauthorized/", permanent=False)    
    
        self.data["user_creation_form"] = user_forms.EditUserForm(instance = user)
        
        profile = user_model.Profile.objects.get(user = user)                
        self.data["profile_form"] = user_forms.ProfileForm(instance = profile)
                
        return render(request, self.template_name, self.data)
        
    #
    #
    def post(self, request, ins = None):
    
        try:
            user = User.objects.get(pk = int(ins))
        except:
            return redirect("/unauthorized/", permanent=False) 
    
        user_form = user_forms.EditUserForm(request.POST, instance = user)
        
        if user_form.is_valid():
            user_form.save()            
            
            profile = user_model.Profile.objects.get(user = user)
                       
            grant_all = request.POST.get("grant_all", False)
            is_create = request.POST.get("is_create", False)
            is_update = request.POST.get("is_update", False)
            is_delete = request.POST.get("is_delete", False)
            is_upload = request.POST.get("is_upload", False)
            
            profile.grant_all = grant_all
            profile.is_create = is_create
            profile.is_update = is_update
            profile.is_delete = is_delete
            profile.is_upload = is_upload
            profile.usertype = request.POST["usertype"]
                
            profile.save()    
                
            self.data["errors"] = []
        else:
            self.data["errors"] = user_form.errors

        return redirect("/edit_user/"+str(ins)+"/",permanent=False)  

#======================================================================
# ManageUser View
#======================================================================
#

class ManageUserView(View):
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/user_management/manage_users.html'

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/user_form.js',]

    data["page_title"] = "Manage Users"
    data["errors"] = []
    data["users_list"] = {}
    
    #
    #
    def get(self, request):    
        self.data["users_list"] = User.objects.all().exclude(is_superuser = True)
        return render(request, self.template_name, self.data)        
  
  
#======================================================================
# Delete User 
#======================================================================
#        

def delete_user(request, ins=None):
    if request.is_ajax() and ins is not None:            
        user = User.objects.get(pk = int(ins))
        user.delete()
    return HttpResponse(0)
        
