# Generated by Django 4.0.3 on 2022-05-19 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_userprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]