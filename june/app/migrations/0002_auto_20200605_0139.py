# Generated by Django 2.2.4 on 2020-06-04 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Company_Table'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'Profile_Table'},
        ),
        migrations.AlterModelOptions(
            name='uploadedfiles',
            options={'verbose_name_plural': 'Uploaded_Files_Table'},
        ),
    ]
