# Generated by Django 5.0.1 on 2024-02-03 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0008_services_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='services',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]