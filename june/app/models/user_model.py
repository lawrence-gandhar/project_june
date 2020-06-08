#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.constants import *


#==========================================================================
#   CHANGE LOGO FILE NAMES
#==========================================================================
#

def logo_rename(instance, filename):

    folder_path = instance.folder_path
    
    upload_path = 'csv_uploads'
    
    if folder_path:
        upload_path = folder_path
    
    ext = filename.split('.')[-1]
    return  os.path.join(upload_path,'{}.{}'.format(uuid4().hex, ext))


#==========================================================================
# PROFILE
#==========================================================================
#

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
    )
    
    usertype = models.IntegerField(
        choices = user_constants.USERTYPE,
        default = 2,
        db_index = True,
        null = False,
    )
    
    grant_all = models.BooleanField(
        choices = user_constants.IS_ACTIVE,
        default = False,
        db_index = True,
        blank = True,
    )
    
    is_create = models.BooleanField(
        choices = user_constants.IS_ACTIVE,
        default = False,
        db_index = True,
        blank = True,
    )
    
    is_update = models.BooleanField(
        choices = user_constants.IS_ACTIVE,
        default = False,
        db_index = True,
        blank = True,
    )
    
    is_delete = models.BooleanField(
        choices = user_constants.IS_ACTIVE,
        default = False,
        db_index = True,
        blank = True,
    )
    
    is_upload = models.BooleanField(
        choices = user_constants.IS_ACTIVE,
        default = False,
        db_index = True,
        blank = True,
    )
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Profile_Table"
   
#==========================================================================
# COMPANY
#==========================================================================
#
   
class Company(models.Model):
    
    user = models.ForeignKey(
        User,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )
    
    company_name = models.CharField(
        max_length = 250,
        blank = False,
        null = False,
    ) 
    
    is_active = models.BooleanField(
        choices = user_constants.IS_ACTIVE,
        default = True,
        db_index = True,
    )
    
    description = models.TextField(
        blank = True,
        null = True,
    ) 
    
    folder_name = models.CharField(
        null = True,
        blank = True,
        max_length = 100,
    )
    
    added_on = models.DateTimeField(
        auto_now_add = True,
        db_index = True,
    )
        
    def __str__(self):
        return self.user.username+" : "+self.company_name
        
    class Meta:
        verbose_name_plural = "Company_Table"    
 
#==========================================================================
# FOLDER LIST MODELS
#==========================================================================
#
 
class FolderList(models.Model):

    company = models.ForeignKey(
        Company,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )
    
    parent_folder = models.ForeignKey(
        'self',
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    folder_name = models.CharField(
        max_length = 250,
        db_index = True,
        blank = False,
        null = True,
    )
    
    added_on = models.DateTimeField(
        auto_now_add = True,
        db_index = True,
    )

    def __str__(self):
        return self.folder_name
        
    class Meta:
        verbose_name_plural = "Folder_List_Table"


 
#==========================================================================
# UPLOADED FILES
#==========================================================================
#
   
class UploadedFiles(models.Model): 
   
    user = models.ForeignKey(
        User,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )
    
    company = models.ForeignKey(
        Company,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )
    
    company_folder = models.BooleanField(
        default = True,
        db_index = True,
    ) 
    
    folder_path = models.ForeignKey(
        FolderList,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )
    
    uploaded_file = models.CharField(
        null = True,
        blank = True,
        max_length = 250,
    )
    
    no_of_rows = models.IntegerField(
        default = 0,
        db_index = True,
    )
    
    def __str__(self):
        return self.user.username+" : "+self.company_name+ " : "+self.uploaded_file.path
    
    class Meta:
        verbose_name_plural = "Uploaded_Files_Table"
 

#==================================================================
# Create instances on User Creation
#==================================================================
#

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        pass