# Generated by Django 5.0.1 on 2024-03-10 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0005_practicemembershipsandaffiliations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='practicemembershipsandaffiliations',
            old_name='date_create',
            new_name='date_created',
        ),
    ]
