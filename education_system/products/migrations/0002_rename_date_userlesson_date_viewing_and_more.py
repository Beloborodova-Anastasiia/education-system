# Generated by Django 4.2 on 2023-09-20 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlesson',
            old_name='date',
            new_name='date_viewing',
        ),
        migrations.RenameField(
            model_name='userlesson',
            old_name='time',
            new_name='viewing_duration',
        ),
    ]
