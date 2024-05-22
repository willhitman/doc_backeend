# Generated by Django 5.0.1 on 2024-03-10 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0003_remove_practice_services_practice_services'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practice',
            name='services',
        ),
        migrations.AddField(
            model_name='practiceservices',
            name='practice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='practice.practice'),
        ),
    ]
