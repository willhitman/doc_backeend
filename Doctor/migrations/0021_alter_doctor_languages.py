# Generated by Django 5.0.1 on 2024-03-21 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0020_delete_insurance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='languages',
            field=models.ManyToManyField(blank=True, to='Doctor.doctorlanguages'),
        ),
    ]