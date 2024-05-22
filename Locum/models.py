from django.db import models


class Locum(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, blank=True)
    national_id = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    linkedin = models.CharField(max_length=50, null=True, blank=True)
    address = models.OneToOneField('address.Address', on_delete=models.CASCADE, blank=True, null=True)
    languages = models.ManyToManyField('LocumLanguages', blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class LocumLanguages(models.Model):
    language = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.language


class LocumSpecialization(models.Model):
    locum = models.ForeignKey(Locum, on_delete=models.CASCADE, null=True, blank=True)
    board_or_certification = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.board_or_certification


class LocumAffiliations(models.Model):
    locum = models.ForeignKey(Locum, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class LocumEducationalBackground(models.Model):
    locum = models.ForeignKey(Locum, on_delete=models.CASCADE)
    school = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return {self.school}
