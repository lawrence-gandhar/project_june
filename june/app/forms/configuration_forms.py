#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.contrib.auth.models import User

from django.forms import *
from app.constants import *
from app.models import * 

#==========================================================================
#   FILE UPLOADING CONFIGURATIONS FORM
#==========================================================================
#

class UploadConfigForm(ModelForm):
    class Meta:
        model = configuration_model.UploadConfig
        fields = ('config_name', 'file_types', 'upload_size', 'size_unit',)

        widgets = {
            'config_name' : TextInput({'attrs':'form-control'}),
            'file_types' : TextInput({'attrs':'form-control', 'placeholder':'xls,csv,xlsx'}),
            'upload_size' : TextInput({'attrs':'form-control'}),
            'size_unit' : Select({'attrs':'form-control'}, choices=file_constants.MEMORY_UNITS),
        }

  
#==========================================================================
#   FILE INFO CONFIGURATIONS FORM
#==========================================================================
#

class FileConfigForm(ModelForm):
    class Meta:
        model = configuration_model.FileConfig
        fields = ('config_name', 'description', 'column_check',)

        widgets = {
            'config_name' : TextInput({'attrs':'form-control'}),
            'description' : Textarea({'attrs':'form-control'}),
            'column_check' : Select({'attrs':'form-control'}, choices=file_constants.COLUMN_CHECK),
        }

#==========================================================================
#   FILE : COLUMNS MAPPING & CONFIGURATIONS FORMS AND FORMSETS
#==========================================================================
#

class ColumnConfigForm(ModelForm):
    model = configuration_model.ColumnConfig
    fields = ('column_name', 'column_dtype', 'column_valid_for', 'column_regex')

    widgets = {
            'column_name' : TextInput({'attrs':'form-control'}),
            'column_dtype' : TextInput({'attrs':'form-control', 'placeholder':'xls,csv,xlsx'}),
            'column_regex' : TextInput({'attrs':'form-control'}),
            'column_valid_for' : Select({'attrs':'form-control'}, choices=file_constants.COLUMN_VALID_FOR),
        }

#
#
ColumnConfigFormset = formset_factory(ColumnConfigForm, extra=1)

#
#
FileColumnConfigFormset = inlineformset_factory(
        configuration_model.FileConfig, configuration_model.ColumnConfig, extra = 1,

        fields = ('column_name', 'column_dtype', 'column_valid_for', 'column_regex'),

        widgets = {
            'column_name' : TextInput({'attrs':'form-control'}),
            'column_dtype' : TextInput({'attrs':'form-control', 'placeholder':'xls,csv,xlsx'}),
            'column_regex' : TextInput({'attrs':'form-control'}),
            'column_valid_for' : Select({'attrs':'form-control'}, choices=file_constants.COLUMN_VALID_FOR),
        }
)