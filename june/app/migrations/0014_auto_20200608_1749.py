# Generated by Django 2.2.4 on 2020-06-08 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20200608_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfiles',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Company'),
        ),
        migrations.AddField(
            model_name='uploadedfiles',
            name='company_folder',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
