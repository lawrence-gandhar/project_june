#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import *
from app.constants import *
from app.models import *

#
#
#
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        
        widgets = {
            'first_name' : TextInput(attrs = {'autofocus':'false', 'class':'form-control', 'required':'true'}),
            'last_name' : TextInput(attrs = {'class':'form-control',}),
            'email' : TextInput(attrs = {'class':'form-control', 'type':'email',}),
            'username' : TextInput(attrs = {  'class':'form-control', 'required':'true', 'autocomplete':'nofill',}),
            'password1' : TextInput(attrs = {'class':'form-control', 'type':'password', 'required':'true'}),
            'password2' : TextInput(attrs = {'class':'form-control', 'type':'password', 'required':'true', }),
        }
        
#
#
#
class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        
        widgets = {
            'username' : TextInput(attrs = {'class':'form-control', 'required':'true', 'readonly':'true'}),
            'first_name' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
            'last_name' : TextInput(attrs = {'class':'form-control',}),
            'email' : TextInput(attrs = {'class':'form-control', 'type':'email',}),   
        }        
            
#
#
#
class ProfileForm(ModelForm):
    
    class Meta:
        model = user_model.Profile

        fields = ('usertype', 'grant_all', 'is_create', 'is_update', 'is_delete', 'is_upload')
        
        widgets = {
            'usertype' : Select(attrs = {'class':'form-control',}, choices = user_constants.USERTYPE), 
            'grant_all' : CheckboxInput(attrs = {'class':'custom-control-input', 'value':'1'},),  
            'is_create' : CheckboxInput(attrs = {'class':'custom-control-input', 'value':'1'},),
            'is_update' : CheckboxInput(attrs = {'class':'custom-control-input', 'value':'1'},), 
            'is_delete' : CheckboxInput(attrs = {'class':'custom-control-input', 'value':'1'},), 
            'is_upload' : CheckboxInput(attrs = {'class':'custom-control-input', 'value':'1'},),
        }
        
#
#
#
class PasswordForm(UserCreationForm):
    class Meta:
        model = User
        
        fields = ('password1', 'password2',)
        
        widgets = {
            'password1' : TextInput(attrs = {'class':'form-control', 'type':'password', 'required':'true'}),
            'password2' : TextInput(attrs = {'class':'form-control', 'type':'password', 'required':'true', }),
        }