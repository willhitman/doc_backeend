# Generated by Django 5.0.1 on 2024-01-23 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('national_id', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('linkedin', models.CharField(max_length=50)),
                ('home_address', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('office_address', models.CharField(max_length=50)),
                ('profile_picture', models.ImageField(upload_to='images/')),
                ('languages', models.CharField(max_length=50)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentsAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.CharField(max_length=50)),
                ('period', models.CharField(max_length=50)),
                ('average_wait_time', models.CharField(max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorAffiliationsAndMemberships',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='files/')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorEducationalBackground',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=50)),
                ('degree', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years_of_experience', models.CharField(max_length=50)),
                ('practice', models.CharField(max_length=50)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.BigIntegerField(help_text='Number of ratings')),
                ('testimonial', models.CharField(max_length=50)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorSpecialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_or_certification', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='files/')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=50)),
                ('doctor_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctorreviews')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorPracticeLocationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_or_hospital', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('contact_phone_number', models.CharField(max_length=50)),
                ('contact_email', models.CharField(max_length=50)),
                ('whatsapp_number', models.CharField(max_length=50)),
                ('office_hours', models.CharField(max_length=50)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
                ('accepted_insurances', models.ManyToManyField(to='Doctor.insurance')),
                ('services', models.ManyToManyField(to='Doctor.services')),
            ],
        ),
    ]
