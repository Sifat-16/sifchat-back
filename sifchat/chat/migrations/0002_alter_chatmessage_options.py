# Generated by Django 4.0.3 on 2022-05-24 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ['-timestamp']},
        ),
    ]
