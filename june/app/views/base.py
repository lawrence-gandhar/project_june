from django.views import View
from django.shortcuts import render

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

#======================================================================
# UnAuthorized View
#======================================================================
#
class UnAuthorized(View):

    def get(self, request):
        template_name = 'app/base/error_page.html'
        return render(request, template_name, {})
        
#======================================================================
# Authentication View
#======================================================================
#
