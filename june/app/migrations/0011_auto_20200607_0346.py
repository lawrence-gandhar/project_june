# Generated by Django 2.2.4 on 2020-06-06 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_company_folder_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folderlist',
            old_name='folder_path',
            new_name='folder_name',
        ),
        migrations.AddField(
            model_name='folderlist',
            name='parent_folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.FolderList'),
        ),
    ]
