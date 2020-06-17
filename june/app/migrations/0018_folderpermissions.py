# Generated by Django 2.2.4 on 2020-06-10 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0017_folderlist_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolderPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.CharField(choices=[(0, 'Grant All'), (1, 'Create'), (2, 'Rename'), (3, 'Replace'), (4, 'Delete'), (5, 'Upload')], db_index=True, default=0, max_length=20)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.FolderList')),
                ('uploaded_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.UploadedFiles')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]