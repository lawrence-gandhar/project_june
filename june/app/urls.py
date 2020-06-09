from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from app.views import *

# Authorization
urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'app/base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'app/base/logout.html'), name = 'logout'),
    re_path(r'^accounts/*', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('unauthorized/', login_required(base.UnAuthorized.as_view()), name = 'unauthorized'),
]    

# User Management
urlpatterns += [
    path('dashboard/', never_cache(login_required(dashboard.DashboardView.as_view())), name = 'dashboard'),
    path('add_user/', never_cache(login_required(user_management.AddUserView.as_view())), name = 'add_user'),
    path('edit_user/<int:ins>/', never_cache(login_required(user_management.EditUserView.as_view())), name = 'edit_user'),
    path('manage_user/', never_cache(login_required(user_management.ManageUserView.as_view())), name = 'manage_user'),
    path('delete_user/<int:ins>/', never_cache(login_required(user_management.delete_user)), name = 'delete_user'),
]

# Company Management
urlpatterns += [
    path('manage_company/', never_cache(login_required(company_management.ManageCompanyView.as_view())), name = 'manage_company'),
    path('add_company/', never_cache(login_required(company_management.add_company)), name = 'add_company'),
    path('edit_company/', never_cache(login_required(company_management.edit_company)), name = 'edit_company'),
    path('delete_company/<int:ins>/', never_cache(login_required(company_management.delete_company)), name = 'delete_company'),
    path('delete_company_folder/<int:ins>/', never_cache(login_required(company_management.delete_company_folder)), name = 'delete_company_folder'),
    path('change_company_status/<int:ins>/<int:status>', never_cache(login_required(company_management.change_company_status)), name = 'change_company_status'),
] 

# Folder Management
urlpatterns += [
    path('manage_folder/<int:company>/', never_cache(login_required(folder_management.ManageFolderView.as_view())), name = 'manage_folder'),
    path('manage_folder/<int:company>/<int:parent_folder>/', never_cache(login_required(folder_management.ManageFolderView.as_view())), name = 'manage_folder'),
    path('delete_folder/<int:ins>/', never_cache(login_required(folder_management.delete_folder)), name = 'delete_folder'),
    path('rename_folder/', never_cache(login_required(folder_management.rename_folder)), name = 'rename_folder'),
] 

# File Management
urlpatterns += [
    path('upload_file/', never_cache(login_required(file_management.upload_file)), name = 'upload_file'),
    path('manage_file/<int:ins>/', never_cache(login_required(file_management.FileView.as_view())), name = 'manage_file'),
    path('delete_file/<int:ins>/', never_cache(login_required(file_management.delete_file)), name = 'delete_file'),
    path('rename_file/<int:ins>/', never_cache(login_required(file_management.rename_file)), name = 'rename_file'),

]    

