# Generated by Django 5.0.1 on 2024-02-21 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Locum', '0002_locum_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocumLanguages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
