import datetime
from django.core.validators import MaxValueValidator
from django.db import models

from Locum.models import Locum
from accounts.models import User
from accounts.service_account_manager import save_user_service_accounts
from address.models import Address, Insurance, Services, Languages
from jobs.models import Jobs


# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    national_id = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    linkedin = models.CharField(max_length=50, null=True, blank=True)
    address = models.OneToOneField(Address, max_length=50, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    languages = models.ManyToManyField('DoctorLanguages', blank=True)

    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name}  {self.user.last_name}'


class DoctorLanguages(models.Model):
    language = models.ForeignKey(Languages, max_length=50, null=True, blank=True, on_delete=models.CASCADE)
    proficiency = models.IntegerField(null=True,blank=True,validators=[MaxValueValidator(10)])

    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.language}'


class DoctorSpecialization(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    board_or_certification = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.board_or_certification


class DoctorAffiliationsAndMemberships(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class DoctorEducationalBackground(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    school = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return {self.school}


Type = (
    ('Clinic', 'Clinic'),
    ('Hospital', 'Hospital')
)


class DoctorExperience(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    years_of_experience = models.CharField(max_length=50, null=True, blank=True)
    practice = models.CharField(max_length=50, null=True, blank=True)

    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.doctor


class AppointmentsAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    days = models.ManyToManyField(to='Days')
    average_wait_time = models.CharField(max_length=50, null=True, blank=True)

    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.days


class Days(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class DoctorReviews(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    # add patient later
    ratings = models.BigIntegerField(help_text='Number of ratings', null=True, blank=True)
    testimonial = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.doctor


class Review(models.Model):
    doctor_review = models.ForeignKey(DoctorReviews, on_delete=models.CASCADE, null=True, blank=True)
    review = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.review


class DoctorsLocum(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True, blank=True)
    date_from = models.DateField(max_length=20, null=True, blank=True)
    date_to = models.DateField(max_length=10, null=True, blank=True)
    employment_type = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(max_length=100, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.job.name


class DoctorService(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    service = models.OneToOneField(Services, on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(max_length=100, default=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.service.name
