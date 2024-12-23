# Generated by Django 5.0.1 on 2024-01-27 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0004_doctorlanguages_date_create_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appointmentsavailability',
            name='days',
            field=models.ManyToManyField(to='Doctor.days'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='languages',
            field=models.ManyToManyField(to='Doctor.doctorlanguages'),
        ),
        migrations.AlterField(
            model_name='doctorpracticelocationinfo',
            name='accepted_insurances',
            field=models.ManyToManyField(to='Doctor.insurance'),
        ),
        migrations.AlterField(
            model_name='doctorpracticelocationinfo',
            name='services',
            field=models.ManyToManyField(to='Doctor.services'),
        ),
    ]
