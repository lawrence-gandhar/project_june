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
import numpy as np

from datetime import datetime

#======================================================================
# Validation Check
#======================================================================
#

def validate_num_field(col_value):
    if col_value!="":
        if type(col_value) == float or type(col_value) == int:
            return True
        return False
    else:
        return True

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
        dest = os.path.join(folder_path,f.name)
        
        filename = f.name
        
        if os.path.exists(dest):
            curr = datetime.now().strftime("%Y%m%d-%H%M%S_")
            dest = os.path.join(folder_path,curr+f.name)
            filename = curr+f.name
                        
        with open(dest, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return filename


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
                filename = handle_uploaded_file(request.FILES['uploaded_file'], comp_ins, parent)  
                
                ins = form.save(commit = False) 
    
                ins.uploaded_file = filename
    
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
                
        return redirect('/manage_file/'+str(ins.id)+"/",permanent=False)
    return redirect("/unauthorized/",permanent=False)

#======================================================================
# File Contents View And Validation
#======================================================================
#
class FileView(View):

    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/file_management/file_view.html'

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/file_management.js']

    data["page_title"] = "Manage File"
    data["errors"] = ""


    #
    #
    #
    def get(self, request, ins=None):
    
        self.data["errors"] = ""
        try:
            file_ins = user_model.UploadedFiles.objects.get(pk = int(ins))  
        except:
            return redirect("/unauthorized/", permanent=False)

        self.data["file_ins"] = file_ins.id
        
        self.data["rename_file_form"] = company_forms.RenameUploadFileForm(instance = file_ins)

        #
        # File Data Show & Validations
        #
        fd = os.path.join(get_file_path(file_ins),file_ins.uploaded_file)

        try:
            df = pd.read_excel(fd, header=0)  
        except:
            self.data["data_html"] = ''
            self.data["errors"] = "Unsupported format, or corrupt file"
            return render(request, self.template_name, self.data)

        numeric_cols = ["SR_GL_CODE","GL_Code","Sales","HUH_Sales","RM",
        "Resource_Cost","Revised_Resource_Cost","Qty_Discount","Export_Ben",
        "Adv_License","Other_direct_material_ML","Other_direct_material_SS",
        "Other_direct_material_Solvent_con","Other_direct_material_Packing",
        "Indirect_material__cyl_abs_","PMD_COGS","Digital_Printer_Ink_Adj","Spec_adj",
        "Cyl_recovery","Cylinder_Profit_Margin","Digital_Printer__Under__Over_Recovery",
        "Printing__Under__Over_Recovery","Lamination__Under___Over_Recovery",
        "HTMelt__Under___Over_Recovery","Slitting__Under___Over_Recovery",
        "SS__Under___Over_Recovery","Packing__Under___Over_Recovery","Metalz__Under___Over_Recovery",
        "Emboss__Under___Over_Recovery","Flexo__Under___Over_Recovery",
        "Jbwrk_Tha__Under___Over_Recovery","Total__Under__Over_Recovery","Scrap_Sales",
        "S_D","CHQ","Inc_Dec_of_Stock","HUH_Cylinder","Misc_Income","Processing_Chg",
        "Inventory_Adjustments","Sales_Forex","RM_Forex","Compensation_Received",
        "Rebates","VA_before_Other_Adjustments","Other_adjustments_for_VA","HUH_sales_with_Sales_Forex",
        "IND_VA","EBIT_w_o_Under_Over","IND_EBIT","Huh_VA","Huh_EBIT_before_Grp_Cost",
        "HUH_GP_before_Adj","Grp_Cost","Huh_EBIT_after_Grp_Cost",
        "Revised_Ind_Sales_with_Rebate_Allocation","Revised_Ind_VA_with_Rebate_Allocation",
        "Revised_Ind_EBIT_with_Rebate_Allocation","Revised_Huh_Sales_with_Rebate_Allocation",
        "Revised_Huh_VA_with_Rebate_Allocation","Revised_Huh_GP_with_Rebate_Allocation",
        "Revised_Huh_EBIT_before_grp_cost_with_Allocation",
        "Revised_Huh_EBIT_after_grp_cost_with_Rebate_Allocation","CUSTOMER_NUMBER","CUSTOMER_TRX_ID",
        "CUSTOMER_TRX_LINE_ID","CONVERSION_FACTOR","QUANTITY_INVOICED","UNIT_SELLING_PRICE",
        "INV_AMT_FC","EXCHANGE_RATE","INV_AMT_INR","ORDERED_QUANTITY2","ACCTD_AMOUNT","GL_CODE",
        "SALES_ORDER","SO_LINE_NO","PRODUCT_GSM","NO_OF_ONS","COIL_WIDTH","QTY_KM","SO_HEADER_ID",
        "SO_LINE_ID","COGS_MATERIAL_COST","COGS_RESOURCE_COST","QTY_SQM","SO_CREA_EXCHANGE_RATE",
        "MIS_COST_RMC","IP_RMA_QTY2","BUD_EXCHANGE_RATE","EXC_CHAP_NO","STD_NO","PMAC_RATE",
        "EBIT_Percent","Contribution","Contribution_Percent","Sales_SQM","VA_SQM",
        "EBIT_SQM","Revised_EBIT_wo_OU","Revised_EBIT_wo_OU_Percent","Net_Sales","VA_Percent",
        "EBIT_Percent_Sales","HUH_Net_Sales","HUH_VA_percent","HUH_EBIT_percent","KSQM","YEAR"]

        list_set = defaultdict()

        for i in numeric_cols:
            
            if i not in df:
                self.data["errors"] = "Column Names Mismatch. Not a correct file"
                self.data["data_html"] = ''
                return render(request, self.template_name, self.data)
            else:
                try:
                    subtex = df.index[df[i].apply(validate_num_field) == False].to_list()  
                    
                    if len(subtex) > 0:
                        for x in subtex:
                            if x in list_set.keys():
                                list_set[x].append(df.columns.get_loc(i))
                            else:
                                list_set[x] = []
                                list_set[x].append(df.columns.get_loc(i))
                except:
                    pass
        
        self.data["wrong_rows_list"] = dict(list_set)

        df.index = np.arange(1, len(df) + 1)
        df= df.fillna("")

        self.data["data_html"] = df.to_html()
        return render(request, self.template_name, self.data)

#======================================================================
# Delete File
#======================================================================
#

def delete_file(request, ins = None):
    if ins is not None:
        try:
            file_ins = user_model.UploadedFiles.objects.get(pk = int(ins))
        except:
            return redirect("/unauthorized/", permanent=False)

        fd = os.path.join(get_file_path(file_ins),file_ins.uploaded_file)
        try:
            os.remove(fd)
        except:
            pass
        company = file_ins.company.id
        parent_folder = None

        if not file_ins.company_folder:
            parent_folder = file_ins.folder_path.id

        file_ins.delete()

        if parent_folder is not None:
            return redirect("/manage_folder/"+str(company)+"/"+str(parent_folder)+"/", permanent=False)
        else:
            return redirect("/manage_folder/"+str(company)+"/", permanent=False)

    return redirect("/unauthorized/", permanent=False)


#======================================================================
# Rename File
#======================================================================
#

def rename_file(request, ins=None):
    if ins is not None:
        try:
            file_ins = user_model.UploadedFiles.objects.get(pk = int(ins))
        except:
            return redirect("/unauthorized/", permanent=False)
        
        fd = get_file_path(file_ins)
        old_path = os.path.join(fd, file_ins.uploaded_file)
        
        form = company_forms.RenameUploadFileForm(request.POST, instance = file_ins)

        if form.is_valid():
    
            fins = form.save(commit=False)
    
            filename = request.POST["uploaded_file"]
    
            new_path = os.path.join(fd, request.POST["uploaded_file"])
            
            if request.POST["uploaded_file"] != file_ins.uploaded_file:
                if os.path.exists(new_path):
                    curr = datetime.now().strftime("%Y%m%d-%H%M%S_")
                    new_path = os.path.join(fd,curr+request.POST["uploaded_file"])
                    filename = curr+request.POST["uploaded_file"]
        
                os.rename(old_path, new_path)
                fins.uploaded_file = filename
                fins.save()
                
        if file_ins.folder_path is not None:
            return redirect("/manage_folder/"+str(file_ins.company.id)+"/"+str(file_ins.folder_path.id)+"/", permanent=False)
        else:
            return redirect("/manage_folder/"+str(file_ins.company.id)+"/", permanent=False)
    return redirect("/unauthorized/", permanent=False)
        
        
        