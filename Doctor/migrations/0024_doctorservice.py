# Generated by Django 5.0.1 on 2024-04-28 11:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0023_alter_doctorlanguages_language_and_more'),
        ('address', '0007_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
                ('service', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.services')),
            ],
        ),
    ]
