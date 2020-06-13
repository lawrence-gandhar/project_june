#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.constants import *

#==========================================================================
#   FILE UPLOADING CONFIGURATIONS
#==========================================================================
#

class UploadConfig(models.Model):
    
    config_name = models.CharField(
        max_length = 100,
        blank = False,
        null = False,
        db_index = True,
        unique = True,
    )
    
    file_types = models.CharField(
        max_length = 250,
        blank = False,
        null = False,
    )
    
    upload_size = models.IntegerField(
        default = 1,
        db_index = True,
    )
    
    size_unit = models.IntegerField(
        choices = file_constants.MEMORY_UNITS,
        default = file_constants.MU_BYTE,
        db_index = True,
    )
    
    def __str__(self):
        return self.config_name
    
    class Meta:
        verbose_name_plural = "Uploaded_Configuration_Table"
  
  
#==========================================================================
#   FILE INFO CONFIGURATIONS
#==========================================================================
#

class FileConfig(models.Model):
    
    upload_config = models.ForeignKey(
        UploadConfig,
        db_index = True,
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
    )
    
    config_name = models.CharField(
        max_length = 100,
        blank = False,
        null = False,
        db_index = True,
        unique = True,
    )
    
    description = models.TextField(
        blank = True,
        null = True,
    )
            
    column_check = models.IntegerField(
        choices = file_constants.COLUMN_CHECK,
        default = file_constants.COLC_STRICT,
        db_index = True,
    )
    
    def __str__(self):
        return self.config_name
    
    class Meta:
        verbose_name_plural = "File_Configuration_Table"
    
  
#==========================================================================
#   FILE : COLUMNS MAPPING & CONFIGURATIONS
#==========================================================================
#

class ColumnConfig(models.Model):   
 
    file_config = models.ForeignKey(
        FileConfig,
        db_index = True,
        null = False,
        blank = False,
        on_delete = models.CASCADE,
    )
 
    column_name = models.CharField(
        max_length = 100,
        blank = False,
        null = False,
        db_index = True,
    )
    
    column_dtype = models.IntegerField(
        choices = file_constants.DTYPES,
        default = file_constants.DT_STRING,
        db_index = True,
    )    

    column_valid_for = models.IntegerField(
        choices = file_constants.COLUMN_VALID_FOR,
        default = file_constants.CVF_ANY,
        db_index = True,
    )    
    
    column_regex = models.TextField(
        blank = True,
        null = True,
    )
    
    def __str__(self):
        return self.column_name
    
    class Meta:
        verbose_name_plural = "Column_Configurations_Table"
    
    
    