# Generated by Django 5.0.1 on 2024-03-12 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_languages_accessibility'),
        ('practice', '0006_rename_date_create_practicemembershipsandaffiliations_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='accessibility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.accessibility'),
        ),
    ]